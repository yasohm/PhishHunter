(function () {
  'use strict';

  const BANNER_ID = 'phishguard-warning-banner';

  async function getSensitivity() {
    return new Promise(resolve => {
      chrome.storage.local.get({ sensitivity: 'suspicious' }, d => resolve(d.sensitivity));
    });
  }

  async function showBanner(result) {
    const { risk_level, confidence } = result;
    if (risk_level === 'safe') return;

    const sensitivity = await getSensitivity();
    if (sensitivity === 'dangerous' && risk_level === 'suspicious') return;

    document.getElementById(BANNER_ID)?.remove();

    const isDangerous = risk_level === 'dangerous';
    const bg     = isDangerous ? '#dc2626' : '#ea580c';
    const border = isDangerous ? '#b91c1c' : '#c2410c';
    const label  = isDangerous ? 'PHISHING DÉTECTÉ' : 'Site Suspect';

    // SVG icons — no emojis
    const iconSvg = isDangerous
      ? `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`
      : `<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`;

    const banner = document.createElement('div');
    banner.id = BANNER_ID;
    banner.setAttribute('style', [
      'all:initial',
      'display:flex',
      'align-items:center',
      'justify-content:space-between',
      'gap:12px',
      'position:fixed',
      'top:0', 'left:0', 'right:0',
      'z-index:2147483647',
      `background:${bg}`,
      `border-bottom:3px solid ${border}`,
      'color:#fff',
      'padding:10px 16px',
      'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif',
      'font-size:14px',
      'box-shadow:0 3px 16px rgba(0,0,0,0.35)',
    ].join(';'));

    banner.innerHTML = `
      <div style="display:flex;align-items:center;gap:10px;flex:1;min-width:0;">
        <span style="flex-shrink:0;display:flex;align-items:center;">${iconSvg}</span>
        <div style="min-width:0;">
          <div style="font-weight:700;font-size:13px;letter-spacing:.06em;">${label}</div>
          <div style="font-size:12px;opacity:.9;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
            ${window.location.hostname} &mdash; Confiance&nbsp;: <strong>${confidence}%</strong>
          </div>
        </div>
      </div>
      <button id="pg-dismiss" style="
        all:initial;cursor:pointer;flex-shrink:0;
        background:rgba(255,255,255,.22);
        border:1px solid rgba(255,255,255,.4);
        color:#fff;padding:5px 13px;border-radius:5px;
        font-size:12px;font-family:inherit;
      ">Ignorer</button>
    `;

    document.documentElement.prepend(banner);
    document.getElementById('pg-dismiss')?.addEventListener('click', () => banner.remove());
  }

  // Listen for messages pushed by service worker
  chrome.runtime.onMessage.addListener(({ type, result }) => {
    if (type === 'PHISHGUARD_RESULT') showBanner(result);
  });

})();
