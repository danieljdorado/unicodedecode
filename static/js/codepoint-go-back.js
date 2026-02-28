/**
 * Codepoint page: whether to show the "Go Back" link based on browser history.
 * Show when there is at least one previous entry (history.length > 1).
 * Exposed as window.codepointGoBack in the browser, or module.exports in Node (for tests).
 */

function shouldShowGoBack() {
  return typeof window !== 'undefined' && window.history != null && window.history.length > 1;
}

function hideGoBackIfNoHistory() {
  if (!shouldShowGoBack()) {
    var el = document.getElementById('go-back-container');
    if (el) el.style.display = 'none';
  }
}

if (typeof window !== 'undefined') {
  window.codepointGoBack = { shouldShowGoBack: shouldShowGoBack, hideGoBackIfNoHistory: hideGoBackIfNoHistory };
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { shouldShowGoBack: shouldShowGoBack, hideGoBackIfNoHistory: hideGoBackIfNoHistory };
}
