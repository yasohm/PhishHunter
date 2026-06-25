import { callAPI } from '../utils/api.js';
import { getFromCache, saveToCache } from '../utils/cache.js';

const SKIP_HOSTNAMES = [
  /^localhost$/,
  /^127\./,
  /^192\.168\./,
  /^10\./,
  /^172\.(1[6-9]|2\d|3[01])\./,
];

function shouldSkip(url) {
  if (!url || !url.startsWith('http')) return true;
  try {
    const { hostname } = new URL(url);
    return SKIP_HOSTNAMES.some(p => p.test(hostname));
  } catch {
    return true;
  }
}

async function isEnabled() {
  const { enabled = true } = await chrome.storage.local.get('enabled');
  return enabled;
}

// Main: fires on every page navigation
chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status !== 'loading') return;
  const url = tab.url;
  if (shouldSkip(url)) return;
  if (!await isEnabled()) return;

  try {
    let result = await getFromCache(url);
    if (!result) {
      result = await callAPI(url);
      await saveToCache(url, result);
    }

    // Store result in session storage so popup can read it
    await chrome.storage.session.set({ [`tab_${tabId}`]: { result, url } });

    updateIcon(tabId, result.risk_level);

    // Notify content script — may fail if page not ready yet (that's OK)
    chrome.tabs.sendMessage(tabId, { type: 'PHISHHUNTER_RESULT', result })
      .catch(() => {});

  } catch (err) {
    console.warn('[PhishHunter] Analysis failed:', err.message);
    updateIcon(tabId, 'unknown');
  }
});

// Answer popup requests for the current tab result
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'GET_TAB_RESULT') {
    chrome.storage.session.get(`tab_${msg.tabId}`).then(data => {
      sendResponse(data[`tab_${msg.tabId}`] ?? null);
    });
    return true; // keep channel open for async response
  }
  if (msg.type === 'RESCAN') {
    chrome.storage.session.remove(`tab_${msg.tabId}`);
    callAPI(msg.url)
      .then(async result => {
        await saveToCache(msg.url, result);
        await chrome.storage.session.set({ [`tab_${msg.tabId}`]: { result, url: msg.url } });
        updateIcon(msg.tabId, result.risk_level);
        chrome.tabs.sendMessage(msg.tabId, { type: 'PHISHHUNTER_RESULT', result }).catch(() => {});
        sendResponse({ ok: true, result });
      })
      .catch(err => sendResponse({ ok: false, error: err.message }));
    return true;
  }
});

// Clean up session on tab close
chrome.tabs.onRemoved.addListener(tabId => {
  chrome.storage.session.remove(`tab_${tabId}`);
});

function updateIcon(tabId, riskLevel) {
  const MAP = {
    safe:       { icon: 'icons/icon-safe-48.png',       title: 'PhishHunter — Sure' },
    suspicious: { icon: 'icons/icon-suspicious-48.png', title: 'PhishHunter — Suspecte' },
    dangerous:  { icon: 'icons/icon-dangerous-48.png',  title: 'PhishHunter — PHISHING DETECTE' },
    unknown:    { icon: 'icons/icon-48.png',             title: 'PhishHunter' },
  };
  const { icon, title } = MAP[riskLevel] ?? MAP.unknown;
  chrome.action.setIcon({ tabId, path: icon });
  chrome.action.setTitle({ tabId, title });
}
