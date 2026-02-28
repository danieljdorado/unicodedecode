/**
 * Decode page: per-row copy in the Character Details table.
 * Clicking the copy icon in the Action column copies that row's character to the clipboard.
 * Exposed as window.decodeCopyChar in the browser, or module.exports in Node (for tests).
 *
 * @param {HTMLTableElement|null} table - The codepoint-details table.
 * @param {{ writeText: (text: string) => Promise<void> }|undefined} clipboard - Optional clipboard API (defaults to navigator.clipboard in browser).
 */
function attachCopyCharHandler(table, clipboard) {
  if (!table) return;
  var clip = clipboard != null ? clipboard : (typeof navigator !== 'undefined' && navigator.clipboard);
  if (!clip) return;
  table.addEventListener('click', function(e) {
    var btn = e.target && e.target.closest('.copy-char-btn');
    if (!btn) return;
    var ch = btn.getAttribute('data-char');
    if (ch == null) return;
    clip.writeText(ch).then(function() {
      if (typeof M !== 'undefined' && M.toast) {
        M.toast({ html: 'Character copied to clipboard', displayLength: 2000 });
      }
    }).catch(function() {
      if (typeof M !== 'undefined' && M.toast) {
        M.toast({ html: 'Could not copy character', displayLength: 2000 });
      }
    });
  });
}

if (typeof window !== 'undefined') {
  window.decodeCopyChar = { attachCopyCharHandler: attachCopyCharHandler };
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { attachCopyCharHandler: attachCopyCharHandler };
}
