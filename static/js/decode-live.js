/**
 * Decode page: update results as the user types (no Examine button).
 * Debounces input, fetches GET ?s=..., and injects #decode-results-container from the response.
 */
(function() {
  var DEBOUNCE_MS = 350;
  var textarea = document.getElementById('textarea1');
  var container = document.getElementById('decode-results-container');
  var form = textarea && textarea.closest('form');

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
    });
  }

  var shareBtn = document.getElementById('share-button');
  if (shareBtn) {
    shareBtn.addEventListener('click', function() {
      var text = textarea.value.trim();
      var url = text
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

  function getDecodeUrl(text) {
    var path = window.location.pathname || '/';
    if (path.indexOf('?') !== -1) path = path.split('?')[0];
    var query = text.trim() ? '?s=' + encodeURIComponent(text) : '';
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
    var url = getDecodeUrl(text);
    fetch(url, { headers: { 'Accept': 'text/html' } })
      .then(function(res) { return res.text(); })
      .then(function(html) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');
        var fetched = doc.getElementById('decode-results-container');
        if (fetched) {
          injectResults(fetched.innerHTML);
        }
        var newUrl = window.location.pathname + (text.trim() ? '?s=' + encodeURIComponent(text) : '');
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, '', newUrl);
        }
      })
      .catch(function() {
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
