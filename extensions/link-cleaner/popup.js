// Link Cleaner — Popup Script

const DEFAULT_PARAMS = [
  'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
  'utm_id', 'fbclid', 'gclid', 'gclsrc', 'dclid',
  'msclkid', 'twclid', 'li_fat_id', '_ga', '_gl',
  'mc_cid', 'mc_eid', 'igshid', 'yclid', 'epik',
  'mkt_tok', '_hsenc', '_hsmi', 'ref', 'source',
  'trk', 'tracking', 'redirect',
];

document.addEventListener('DOMContentLoaded', async () => {
  const enabledToggle = document.getElementById('enabledToggle');
  const useDefaults = document.getElementById('useDefaults');
  const defaultParamsList = document.getElementById('defaultParamsList');
  const customParamInput = document.getElementById('customParamInput');
  const addParamBtn = document.getElementById('addParamBtn');
  const customTags = document.getElementById('customTags');

  // ── Load state ──
  const state = await chrome.storage.sync.get({
    enabled: true,
    useDefaults: true,
    customParams: [],
  });

  enabledToggle.checked = state.enabled;
  useDefaults.checked = state.useDefaults;

  // ── Populate default params ──
  function renderDefaults() {
    defaultParamsList.innerHTML = '';
    // Show first 20 defaults with checkboxes
    const shown = DEFAULT_PARAMS.slice(0, 25);
    shown.forEach(param => {
      const label = document.createElement('label');
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = state.useDefaults;
      cb.disabled = !state.useDefaults;
      cb.dataset.param = param;
      label.appendChild(cb);
      label.appendChild(document.createTextNode(param));
      defaultParamsList.appendChild(label);
    });
    if (DEFAULT_PARAMS.length > 25) {
      const more = document.createElement('div');
      more.style.cssText = 'color:#8b949e;font-size:11px;padding:4px;text-align:center;';
      more.textContent = `...and ${DEFAULT_PARAMS.length - 25} more tracking params`;
      defaultParamsList.appendChild(more);
    }
  }
  renderDefaults();

  // ── Custom params tags ──
  function renderCustomTags() {
    customTags.innerHTML = '';
    state.customParams.forEach((param, i) => {
      const tag = document.createElement('span');
      tag.className = 'custom-tag';
      tag.innerHTML = `${param} <span class="remove" data-index="${i}">×</span>`;
      customTags.appendChild(tag);
    });

    // Add remove handlers
    document.querySelectorAll('.custom-tag .remove').forEach(el => {
      el.addEventListener('click', () => {
        const idx = parseInt(el.dataset.index);
        state.customParams.splice(idx, 1);
        saveState();
        renderCustomTags();
      });
    });
  }
  renderCustomTags();

  // ── Save state ──
  async function saveState() {
    await chrome.storage.sync.set({
      enabled: enabledToggle.checked,
      useDefaults: useDefaults.checked,
      customParams: state.customParams,
    });
  }

  // ── Event listeners ──
  enabledToggle.addEventListener('change', saveState);

  useDefaults.addEventListener('change', () => {
    state.useDefaults = useDefaults.checked;
    renderDefaults();
    saveState();
  });

  addParamBtn.addEventListener('click', () => {
    const val = customParamInput.value.trim().toLowerCase();
    if (!val) return;
    if (state.customParams.includes(val)) {
      customParamInput.value = '';
      return;
    }
    state.customParams.push(val);
    customParamInput.value = '';
    saveState();
    renderCustomTags();
  });

  customParamInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addParamBtn.click();
  });
});
