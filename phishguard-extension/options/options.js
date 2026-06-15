import { clearCache, getCacheStats } from '../utils/cache.js';

const DEFAULTS = {
  apiUrl: 'http://localhost:8000',
  sensitivity: 'suspicious',
  cacheMinutes: 30,
  enabled: true,
};

async function loadSettings() {
  const s = await chrome.storage.local.get(DEFAULTS);

  document.getElementById('enabled').checked = s.enabled;
  document.getElementById('api-url').value = s.apiUrl;
  document.getElementById('cache-minutes').value = s.cacheMinutes;
  document.getElementById('cache-value').textContent = `${s.cacheMinutes} min`;

  const radio = document.querySelector(`input[name="sensitivity"][value="${s.sensitivity}"]`);
  if (radio) radio.checked = true;

  const stats = await getCacheStats();
  document.getElementById('cache-count').textContent = stats.count;
}

async function saveSettings() {
  const sensitivity = document.querySelector('input[name="sensitivity"]:checked')?.value ?? 'suspicious';
  const settings = {
    enabled:      document.getElementById('enabled').checked,
    apiUrl:       document.getElementById('api-url').value.trim() || DEFAULTS.apiUrl,
    sensitivity,
    cacheMinutes: parseInt(document.getElementById('cache-minutes').value, 10),
  };
  await chrome.storage.local.set(settings);

  const status = document.getElementById('save-status');
  status.textContent = '✓ Paramètres enregistrés';
  setTimeout(() => { status.textContent = ''; }, 2500);
}

async function testConnection() {
  const url = document.getElementById('api-url').value.trim() || DEFAULTS.apiUrl;
  const statusEl = document.getElementById('test-status');
  statusEl.textContent = 'Test…';
  statusEl.className = '';
  try {
    const res = await fetch(`${url}/health`, { signal: AbortSignal.timeout(5000) });
    if (res.ok) {
      statusEl.textContent = '✓ Connecté';
      statusEl.className = 'ok';
    } else {
      throw new Error(`HTTP ${res.status}`);
    }
  } catch (e) {
    statusEl.textContent = `✗ Échec (${e.message})`;
    statusEl.className = 'err';
  }
}

// Range label
document.getElementById('cache-minutes').addEventListener('input', e => {
  document.getElementById('cache-value').textContent = `${e.target.value} min`;
});

document.getElementById('btn-save').addEventListener('click', saveSettings);
document.getElementById('btn-test').addEventListener('click', testConnection);
document.getElementById('btn-clear-cache').addEventListener('click', async () => {
  await clearCache();
  document.getElementById('cache-count').textContent = '0';
});

loadSettings();
