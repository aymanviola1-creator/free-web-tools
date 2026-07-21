// Link Cleaner — Background Service Worker
// Strips tracking parameters from copied URLs

const DEFAULT_TRACKING_PARAMS = [
  // Google Analytics / Campaign
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
  'utm_id', 'utm_cid', 'utm_reader', 'utm_viz_id', 'utm_pubreferrer',
  // Facebook
  'fbclid', 'fb_source', 'fb_ref', 'fb_action_ids', 'fb_action_types',
  'fb_source', 'fb_id',
  // Google Ads / Click IDs
  'gclid', 'gclsrc', 'dclid',
  // Microsoft / Bing
  'msclkid', 'msads',
  // Twitter/X
  'twclid',
  // LinkedIn
  'li_fat_id',
  // HubSpot
  'hsa_cam', 'hsa_grp', 'hsa_mt', 'hsa_src', 'hsa_ad', 'hsa_acc',
  'hsa_net', 'hsa_ver', 'hsa_la', 'hsa_kw',
  // Mailchimp
  'mc_cid', 'mc_eid',
  // Other analytics
  '_ga', '_gl', 'icid', 'vero_conv', 'vero_id',
  'yclid', 'igshid',
  // Pinterest
  'epik', 'pp',
  // Oracle / Eloqua
  'elq_cid', 'elq_ak',
  // Marketo
  'mkt_tok',
  // HubSpot
  '_hsenc', '_hsmi',
  // Outbrain / Taboola
  'ob_cid', 'ob_lang', 'ob_orig_url', 'ob_tw',
  'tb_visibility',
  // Misc tracking
  'ref', 'source', 'pk_source', 'pk_medium', 'pk_campaign', 'pk_keyword',
  'redirect', 'track', 'tracking', 'trk', 'trkCampaign',
];

// ── Clean URL function ──
function cleanURL(url, paramsToStrip = null) {
  try {
    const urlObj = new URL(url);
    const params = paramsToStrip || DEFAULT_TRACKING_PARAMS;

    let cleaned = false;
    for (const param of params) {
      if (urlObj.searchParams.has(param)) {
        urlObj.searchParams.delete(param);
        cleaned = true;
      }
    }

    if (cleaned) {
      // Reconstruct URL without the cleaned params
      let result = urlObj.origin + urlObj.pathname;
      if (urlObj.searchParams.toString()) {
        result += '?' + urlObj.searchParams.toString();
      }
      if (urlObj.hash) {
        result += urlObj.hash;
      }
      return { cleaned: true, url: result };
    }

    return { cleaned: false, url };
  } catch {
    // Invalid URL, return as-is
    return { cleaned: false, url };
  }
}

// ── Get params to strip from storage ──
async function getParamsToStrip() {
  const result = await chrome.storage.sync.get({
    customParams: [],
    enabled: true,
    useDefaults: true,
  });

  let params = [];
  if (result.useDefaults) {
    params = [...DEFAULT_TRACKING_PARAMS];
  }
  if (result.customParams && result.customParams.length > 0) {
    params = [...params, ...result.customParams.map(p => p.trim().toLowerCase()).filter(p => p)];
  }
  return { params, enabled: result.enabled };
}

// ── Listen for messages from content script ──
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'CLEAN_URL') {
    getParamsToStrip().then(({ params, enabled }) => {
      if (!enabled) {
        sendResponse({ cleaned: false, url: request.url });
        return;
      }
      const result = cleanURL(request.url, params);
      if (result.cleaned) {
        // Update badge
        chrome.action.setBadgeText({ text: '✓', tabId: sender.tab?.id });
        chrome.action.setBadgeBackgroundColor({ color: '#3fb950', tabId: sender.tab?.id });
        setTimeout(() => {
          chrome.action.setBadgeText({ text: '', tabId: sender.tab?.id });
        }, 3000);
      }
      sendResponse(result);
    });
    return true; // Keep message channel open for async response
  }

  if (request.type === 'GET_DEFAULTS') {
    sendResponse({ params: DEFAULT_TRACKING_PARAMS });
    return true;
  }
});

// ── Context menu ──
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'cleanLink',
    title: 'Copy Clean Link',
    contexts: ['link'],
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'cleanLink' && info.linkUrl) {
    getParamsToStrip().then(({ params, enabled }) => {
      if (!enabled) {
        navigator.clipboard.writeText(info.linkUrl);
        return;
      }
      const result = cleanURL(info.linkUrl, params);
      const finalURL = result.cleaned ? result.url : info.linkUrl;

      // We can't use clipboard API from background directly, send to content script
      chrome.tabs.sendMessage(tab.id, {
        type: 'COPY_TO_CLIPBOARD',
        text: finalURL,
        cleaned: result.cleaned,
      }).catch(() => {
        // Fallback: if content script not available
        console.log('Would copy:', finalURL);
      });
    });
  }
});
