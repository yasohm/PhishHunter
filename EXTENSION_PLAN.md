# PhishGuard Browser Extension — Implementation Plan

## Overview

A Chrome/Firefox extension that checks every URL you visit in real-time against
the PhishGuard backend API and warns you before a phishing page loads.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Browser Extension                    │
│                                                         │
│  ┌──────────────┐   ┌───────────────┐   ┌───────────┐   │
│  │   Popup UI   │   │  Background   │   │  Content  │   │
│  │              │   │Service Worker │   │  Script   │   │
│  │ - Page score │◄──│               │──►│           │   │
│  │ - History    │   │ - Intercepts  │   │ - Injects │   │
│  │ - Settings   │   │   navigation  │   │  warning  │   │
│  └──────────────┘   │ - Calls API   │   │  banner   │   │
│                     │ - Caches hits │   └───────────┘   │
│                     └───────┬───────┘                   │
└─────────────────────────────┼───────────────────────────┘
                              │ HTTP
                              ▼
                   ┌─────────────────────┐
                   │  PhishGuard Backend │
                   │  POST /api/analyze  │
                   └─────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Manifest | **Manifest V3** | Required for Chrome; supported by Firefox 109+ |
| UI (Popup) | **Preact + Tailwind CDN** | Tiny bundle, same CSS as main app |
| Background | **Service Worker (JS)** | MV3 standard, persistent via chrome.storage |
| Content Script | **Vanilla JS + injected CSS** | No framework needed for a banner |
| Build | **Vite + CRXJS plugin** | Hot reload in dev, proper MV3 bundling |
| Storage | **chrome.storage.local** | Persists cache and settings across sessions |

---

## File Structure

```
phishguard-extension/
├── manifest.json              # MV3 manifest
├── package.json
├── vite.config.js
├── src/
│   ├── background/
│   │   └── service-worker.js  # Core logic: intercept + call API
│   ├── content/
│   │   └── content-script.js  # Inject warning banner into page DOM
│   ├── popup/
│   │   ├── index.html
│   │   ├── Popup.jsx          # Main popup component
│   │   └── main.jsx
│   ├── options/
│   │   ├── index.html
│   │   └── Options.jsx        # Backend URL + sensitivity settings
│   └── utils/
│       ├── api.js             # Fetch wrapper for PhishGuard API
│       └── cache.js           # LRU cache using chrome.storage
├── icons/
│   ├── icon-16.png
│   ├── icon-48.png
│   └── icon-128.png
└── dist/                      # Built extension (load this in Chrome)
```

---

## manifest.json

```json
{
  "manifest_version": 3,
  "name": "PhishGuard",
  "version": "1.0.0",
  "description": "Real-time phishing detection powered by AI",
  "permissions": [
    "tabs",
    "storage",
    "declarativeNetRequest"
  ],
  "host_permissions": [
    "http://localhost:8000/*",
    "<all_urls>"
  ],
  "background": {
    "service_worker": "src/background/service-worker.js",
    "type": "module"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["src/content/content-script.js"],
      "run_at": "document_start"
    }
  ],
  "action": {
    "default_popup": "src/popup/index.html",
    "default_icon": {
      "16":  "icons/icon-16.png",
      "48":  "icons/icon-48.png",
      "128": "icons/icon-128.png"
    }
  },
  "options_ui": {
    "page": "src/options/index.html",
    "open_in_tab": true
  },
  "icons": {
    "16":  "icons/icon-16.png",
    "48":  "icons/icon-48.png",
    "128": "icons/icon-128.png"
  }
}
```

---

## Core Logic

### 1. Service Worker (`background/service-worker.js`)

Listens for every tab navigation, checks the URL against the API, then
broadcasts the result to the content script and updates the extension icon.

```js
// Fires on every page navigation
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status !== 'loading' || !tab.url?.startsWith('http')) return;

  const cached = await getFromCache(tab.url);
  const result = cached ?? await callPhishGuardAPI(tab.url);

  if (!cached) await saveToCache(tab.url, result);

  // Color the extension icon based on risk
  updateIcon(tabId, result.risk_level);

  // Tell the content script to show/hide a warning banner
  chrome.tabs.sendMessage(tabId, { type: 'PHISHGUARD_RESULT', result });
});

async function callPhishGuardAPI(url) {
  const settings = await chrome.storage.local.get({ apiUrl: 'http://localhost:8000' });
  const res = await fetch(`${settings.apiUrl}/api/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  return res.json();
}

function updateIcon(tabId, riskLevel) {
  const icons = {
    safe:       { path: 'icons/icon-safe-48.png',      title: 'PhishGuard — Sûre' },
    suspicious: { path: 'icons/icon-suspicious-48.png', title: 'PhishGuard — Suspecte' },
    dangerous:  { path: 'icons/icon-dangerous-48.png',  title: 'PhishGuard — DANGEREUSE' },
  };
  const { path, title } = icons[riskLevel] ?? icons.safe;
  chrome.action.setIcon({ tabId, path });
  chrome.action.setTitle({ tabId, title });
}
```

### 2. Content Script (`content/content-script.js`)

Injected into every page. Listens for the service worker result and injects
a dismissible warning banner at the top of the page for dangerous/suspicious URLs.

```js
chrome.runtime.onMessage.addListener(({ type, result }) => {
  if (type !== 'PHISHGUARD_RESULT') return;
  if (result.risk_level === 'safe') return;

  const existing = document.getElementById('phishguard-banner');
  if (existing) existing.remove();

  const banner = document.createElement('div');
  banner.id = 'phishguard-banner';
  banner.style.cssText = `
    position: fixed; top: 0; left: 0; right: 0; z-index: 2147483647;
    background: ${result.risk_level === 'dangerous' ? '#dc2626' : '#ea580c'};
    color: white; padding: 10px 20px;
    font-family: sans-serif; font-size: 14px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
  `;
  banner.innerHTML = `
    <span>
      <strong>PhishGuard:</strong>
      ${result.risk_level === 'dangerous' ? 'PHISHING DÉTECTÉ' : 'Site suspect'}
      — Confiance: ${result.confidence}%
    </span>
    <button onclick="this.parentElement.remove()"
      style="background:rgba(255,255,255,0.2); border:none; color:white;
             padding:4px 10px; border-radius:4px; cursor:pointer; font-size:13px;">
      Ignorer
    </button>
  `;
  document.documentElement.prepend(banner);
});
```

### 3. Popup UI (`popup/Popup.jsx`)

Shows the result for the currently active tab. Uses the same design language
as the main PhishGuard app (risk colors, confidence score).

**Displays:**
- Current URL verdict + confidence gauge
- Last 5 scans from `chrome.storage.local`
- Link to open Options page

### 4. Options Page (`options/Options.jsx`)

User-configurable settings stored in `chrome.storage.local`:

| Setting | Default | Description |
|---|---|---|
| `apiUrl` | `http://localhost:8000` | PhishGuard backend URL |
| `sensitivity` | `suspicious` | Minimum level to show banner (`suspicious` or `dangerous`) |
| `cacheMinutes` | `30` | How long to cache a URL result |
| `enabled` | `true` | Global on/off switch |

---

## URL Cache Strategy

Every analyzed URL is stored in `chrome.storage.local` with a TTL to avoid
hammering the API on every page refresh.

```js
// cache.js
const CACHE_KEY = 'phishguard_cache';

export async function getFromCache(url) {
  const { phishguard_cache: cache = {} } = await chrome.storage.local.get(CACHE_KEY);
  const entry = cache[url];
  if (!entry) return null;
  if (Date.now() > entry.expiresAt) return null;  // expired
  return entry.result;
}

export async function saveToCache(url, result) {
  const settings = await chrome.storage.local.get({ cacheMinutes: 30 });
  const { phishguard_cache: cache = {} } = await chrome.storage.local.get(CACHE_KEY);

  // Evict oldest entries if cache exceeds 500 URLs
  const keys = Object.keys(cache);
  if (keys.length >= 500) {
    const oldest = keys.sort((a, b) => cache[a].savedAt - cache[b].savedAt).slice(0, 50);
    oldest.forEach((k) => delete cache[k]);
  }

  cache[url] = { result, savedAt: Date.now(), expiresAt: Date.now() + settings.cacheMinutes * 60_000 };
  await chrome.storage.local.set({ [CACHE_KEY]: cache });
}
```

---

## Icon States

Three colored variants of the PhishGuard icon to give instant visual feedback
in the browser toolbar:

| Icon | Color | Meaning |
|---|---|---|
| `icon-safe.png` | Green shield | URL is safe |
| `icon-suspicious.png` | Orange shield | URL is suspicious |
| `icon-dangerous.png` | Red shield | Phishing detected |

---

## Build & Installation

### Development

```bash
cd phishguard-extension
npm install
npm run dev       # Vite with CRXJS hot-reload
```

Load in Chrome:
1. Go to `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked** → select the `dist/` folder

Load in Firefox:
1. Go to `about:debugging`
2. Click **This Firefox** → **Load Temporary Add-on**
3. Select `dist/manifest.json`

### Production Build

```bash
npm run build
# Creates dist/ — zip it to publish on Chrome Web Store / Firefox Add-ons
```

---

## Implementation Phases

### Phase 1 — Core (3–4 days)
- [ ] Project scaffold with Vite + CRXJS
- [ ] `manifest.json` with correct permissions
- [ ] Service worker: tab listener + API call
- [ ] Content script: warning banner
- [ ] 3 icon variants (safe / suspicious / dangerous)

### Phase 2 — Popup UI (2 days)
- [ ] Popup showing current tab's verdict + confidence
- [ ] Mini scan history (last 5 URLs)
- [ ] Manual "Re-scan this page" button

### Phase 3 — Settings & Cache (1–2 days)
- [ ] Options page (API URL, sensitivity, cache TTL)
- [ ] LRU cache in `chrome.storage.local`
- [ ] Global enable/disable toggle

### Phase 4 — Polish (1 day)
- [ ] Loading state while API responds
- [ ] Offline graceful fallback (no banner if API unreachable)
- [ ] Firefox cross-browser compatibility check

**Total estimated effort: ~7–9 days**

---

## Key Constraints

- **CORS**: The backend must allow the extension origin. Add
  `chrome-extension://*` and `moz-extension://*` to `allow_origins` in
  `backend/main.py`.
- **MV3 service workers** are terminated when idle — do not rely on in-memory
  state; use `chrome.storage` for everything persistent.
- **Private URLs** (intranet, `localhost`) should be skipped to avoid leaking
  internal addresses to the API.
- **HTTPS backend**: When publishing to the Chrome Web Store, the extension
  must call an HTTPS endpoint — a self-signed cert won't work. You'd need to
  deploy the backend with a real domain + TLS.
