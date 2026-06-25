import { getRecentScans } from '../utils/cache.js';

const RISK_LABELS = { safe: 'SÛRE', suspicious: 'SUSPECTE', dangerous: 'DANGEREUSE' };

function show(id)  { document.getElementById(id)?.classList.remove('hidden'); }
function hide(id)  { document.getElementById(id)?.classList.add('hidden'); }

function renderResult(url, result) {
  const { risk_level, confidence } = result;

  hide('state-loading');
  hide('state-unavailable');
  hide('state-error');

  document.getElementById('result-url').textContent = url;

  const badge = document.getElementById('result-badge');
  badge.textContent = RISK_LABELS[risk_level] ?? risk_level.toUpperCase();
  badge.className = risk_level;

  document.getElementById('result-confidence').textContent = `${confidence}%`;

  const bar = document.getElementById('result-bar');
  bar.className = `progress-bar ${risk_level}`;
  bar.style.width = `${confidence}%`;

  show('state-result');
  document.getElementById('btn-rescan').disabled = false;
}

async function renderHistory() {
  const scans = await getRecentScans(5);
  const list = document.getElementById('history-list');

  if (!scans.length) {
    list.innerHTML = '<p class="empty-msg">Aucune analyse pour le moment.</p>';
    return;
  }

  list.innerHTML = scans.map(s => `
    <div class="history-item">
      <div class="h-dot ${s.risk_level}"></div>
      <span class="h-url">${s.url}</span>
      <span class="h-conf">${s.confidence}%</span>
    </div>
  `).join('');
}

async function init() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  if (!tab?.url?.startsWith('http')) {
    hide('state-loading');
    show('state-unavailable');
    await renderHistory();
    return;
  }

  // Ask service worker for cached result
  const data = await chrome.runtime.sendMessage({ type: 'GET_TAB_RESULT', tabId: tab.id });

  if (data?.result) {
    renderResult(data.url ?? tab.url, data.result);
  } else {
    // No result yet — trigger analysis inline
    try {
      const { callAPI } = await import('../utils/api.js');
      const result = await callAPI(tab.url);
      renderResult(tab.url, result);
      // Notify service worker to store + update icon
      chrome.runtime.sendMessage({ type: 'RESCAN', tabId: tab.id, url: tab.url });
    } catch {
      hide('state-loading');
      show('state-error');
    }
  }

  await renderHistory();

  document.getElementById('btn-rescan').addEventListener('click', async () => {
    document.getElementById('btn-rescan').disabled = true;
    hide('state-result');
    show('state-loading');

    chrome.runtime.sendMessage({ type: 'RESCAN', tabId: tab.id, url: tab.url }, (resp) => {
      if (resp?.ok) {
        renderResult(tab.url, resp.result);
        renderHistory();
      } else {
        hide('state-loading');
        show('state-error');
      }
    });
  });
}

document.getElementById('btn-options').addEventListener('click', () => {
  chrome.runtime.openOptionsPage();
});

init();
