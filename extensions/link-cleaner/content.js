// Link Cleaner — Content Script
// Intercepts copy events to clean tracking parameters from URLs

(function() {
  'use strict';

  // ── Check if text looks like a URL ──
  function looksLikeURL(text) {
    return /^https?:\/\/[^\s]+$/.test(text.trim());
  }

  // ── Ask background to clean URL ──
  function cleanURL(url) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage(
        { type: 'CLEAN_URL', url },
        (response) => {
          if (chrome.runtime.lastError) {
            resolve({ cleaned: false, url });
          } else {
            resolve(response);
          }
        }
      );
    });
  }

  // ── Handle copy events ──
  document.addEventListener('copy', async (e) => {
    const selection = window.getSelection().toString().trim();

    if (!looksLikeURL(selection)) {
      return; // Not a URL, let it copy normally
    }

    const result = await cleanURL(selection);

    if (result.cleaned) {
      // Override clipboard with cleaned URL
      e.clipboardData.setData('text/plain', result.url);
      e.preventDefault();

      // Show a brief visual indicator
      showCleanedIndicator();
    }
  });

  // ── Listen for copy-to-clipboard commands from background ──
  chrome.runtime.onMessage.addListener((request) => {
    if (request.type === 'COPY_TO_CLIPBOARD') {
      navigator.clipboard.writeText(request.text).then(() => {
        if (request.cleaned) {
          showCleanedIndicator();
        }
      });
    }
  });

  // ── Visual indicator ──
  function showCleanedIndicator() {
    const indicator = document.createElement('div');
    indicator.textContent = '🔗 Link Cleaned';
    Object.assign(indicator.style, {
      position: 'fixed',
      bottom: '20px',
      right: '20px',
      background: '#238636',
      color: '#fff',
      padding: '8px 16px',
      borderRadius: '6px',
      fontSize: '14px',
      fontFamily: '-apple-system, sans-serif',
      zIndex: 999999,
      boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
      transition: 'opacity 0.3s ease',
      opacity: '1',
      pointerEvents: 'none',
    });

    document.body.appendChild(indicator);
    setTimeout(() => {
      indicator.style.opacity = '0';
      setTimeout(() => indicator.remove(), 300);
    }, 2000);
  }
})();
