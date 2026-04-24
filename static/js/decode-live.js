/**
 * Decode page: update results as the user types (no Examine button).
 * Debounces input, posts form data, and injects #decode-results-container fragment.
 */
(function() {
  var DEBOUNCE_MS = 350;
  var textarea = document.getElementById('textarea1');
  var container = document.getElementById('decode-results-container');
  var form = textarea && textarea.closest('form');
  var latestRequestId = 0;
  var activeController = null;

  if (!textarea || !container) return;

  var homeFeatures = document.getElementById('home-features');
  function toggleHomeFeatures() {
    if (homeFeatures) {
      homeFeatures.style.display = textarea.value.trim() ? 'none' : '';
    }
  }
  toggleHomeFeatures();

  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      updateResults();
    });
  }

  var shareBtn = document.getElementById('share-button');
  if (shareBtn) {
    shareBtn.addEventListener('click', function() {
      var text = textarea.value;
      var url = text.length
        ? window.location.origin + (window.location.pathname || '/') + '?s=' + encodeURIComponent(text)
        : window.location.origin + (window.location.pathname || '/');
      navigator.clipboard.writeText(url).then(function() {
        if (typeof M !== 'undefined' && M.toast) {
          M.toast({ html: 'Link copied to clipboard', displayLength: 2000 });
        } else {
          shareBtn.textContent = 'Copied!';
          setTimeout(function() { shareBtn.innerHTML = '<i class="material-icons left">share</i>Share'; }, 1500);
        }
      }).catch(function() {
        if (typeof M !== 'undefined' && M.toast) {
          M.toast({ html: 'Could not copy link', displayLength: 2000 });
        }
      });
    });
  }

  function getDecodeUrlForHistory(text) {
    var path = window.location.pathname || '/';
    if (path.indexOf('?') !== -1) path = path.split('?')[0];
    var query = text.length ? '?s=' + encodeURIComponent(text) : '';
    return path + query;
  }

  function injectResults(html) {
    container.innerHTML = html;
    var table = document.getElementById('codepoint-details-table');
    if (table && window.decodeCopyChar) {
      window.decodeCopyChar.attachCopyCharHandler(table);
    }
    if (window.decodeClipboard && window.decodeClipboard.attachCopyTableButton) {
      window.decodeClipboard.attachCopyTableButton();
    }
  }

  function updateResults() {
    var text = textarea.value;
    if (!text.length) {
      container.innerHTML = '';
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, '', window.location.pathname);
      }
      return;
    }

    latestRequestId += 1;
    var requestId = latestRequestId;
    if (activeController) activeController.abort();
    activeController = typeof AbortController !== 'undefined' ? new AbortController() : null;

    var csrfInput = form && form.querySelector('input[name="csrfmiddlewaretoken"]');
    var csrfToken = csrfInput ? csrfInput.value : '';
    var body = new URLSearchParams();
    body.append('text', text);
    if (csrfToken) body.append('csrfmiddlewaretoken', csrfToken);

    fetch(form ? form.action : window.location.pathname, {
      method: 'POST',
      headers: {
        'Accept': 'text/html',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Decode-Live': '1',
      },
      body: body.toString(),
      signal: activeController ? activeController.signal : undefined,
    })
      .then(function(res) { return res.text(); })
      .then(function(html) {
        if (requestId !== latestRequestId) return;
        injectResults(html);
        var newUrl = getDecodeUrlForHistory(text);
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, '', newUrl);
        }
      })
      .catch(function(err) {
        if (err && err.name === 'AbortError') return;
        if (typeof M !== 'undefined' && M.toast) {
          M.toast({ html: 'Could not update results', displayLength: 2000 });
        }
      });
  }

  var debounceTimer;
  textarea.addEventListener('input', function() {
    toggleHomeFeatures();
    if (debounceTimer) clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function() {
      debounceTimer = null;
      updateResults();
    }, DEBOUNCE_MS);
  });
})();
