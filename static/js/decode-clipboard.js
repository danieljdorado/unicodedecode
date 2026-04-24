/**
 * Clipboard helpers for the decode page: escapeHtml, cellText, tableToTsv, tableToHtml.
 * Exposed as window.decodeClipboard in the browser, or module.exports in Node (for tests).
 */

/** Escapes HTML special characters in a string (e.g. for use inside tags). */
function escapeHtml(s) {
  var div = document.createElement('div');
  div.textContent = s;
  return div.innerHTML;
}

/** Returns HTML for a table cell: preserves <a href="..."> in the Name column, else escaped text. */
function cellText(cell) {
  var a = cell.querySelector('a');
  if (a && a.href) {
    return '<a href="' + escapeHtml(a.href) + '">' + escapeHtml((a.textContent || '').trim()) + '</a>';
  }
  return escapeHtml((cell.textContent || '').trim());
}

/** Serializes the table as tab-separated values (one row per line) for plain-text paste. */
function tableToTsv(el) {
  var rows = [];
  var headerRow = el.querySelector('thead tr');
  if (headerRow) {
    rows.push(Array.from(headerRow.querySelectorAll('th')).map(function(c) { return (c.textContent || '').trim(); }).join('\t'));
  }
  el.querySelectorAll('tbody tr').forEach(function(tr) {
    rows.push(Array.from(tr.querySelectorAll('td')).map(function(c) { return (c.textContent || '').trim(); }).join('\t'));
  });
  return rows.join('\n');
}

/** Serializes the table as HTML with links preserved so Excel/Sheets keep hyperlinks. */
function tableToHtml(el) {
  var html = '<meta charset="UTF-8"><table><thead><tr>';
  var headerRow = el.querySelector('thead tr');
  if (headerRow) {
    headerRow.querySelectorAll('th').forEach(function(th) {
      html += '<th>' + escapeHtml((th.textContent || '').trim()) + '</th>';
    });
  }
  html += '</tr></thead><tbody>';
  el.querySelectorAll('tbody tr').forEach(function(tr) {
    html += '<tr>';
    tr.querySelectorAll('td').forEach(function(td) {
      html += '<td>' + cellText(td) + '</td>';
    });
    html += '</tr>';
  });
  html += '</tbody></table>';
  return html;
}

/** Attach click handler to #copy-table-button to copy the Character Details table as TSV+HTML. Call after injecting new results. */
function attachCopyTableButton() {
  var copyTableBtn = document.getElementById('copy-table-button');
  var table = document.getElementById('codepoint-details-table');
  if (!copyTableBtn || !table || !window.decodeClipboard) return;
  var decodeClipboard = window.decodeClipboard;
  copyTableBtn.addEventListener('click', function() {
    var tsv = decodeClipboard.tableToTsv(table);
    var html = decodeClipboard.tableToHtml(table);
    if (!tsv) return;
    var item = new ClipboardItem({
      'text/plain': new Blob([tsv], { type: 'text/plain' }),
      'text/html': new Blob([html], { type: 'text/html' })
    });
    navigator.clipboard.write([item]).then(function() {
      if (typeof M !== 'undefined' && M.toast) {
        M.toast({ html: 'Table copied to clipboard', displayLength: 2000 });
      }
    }).catch(function() {
      if (typeof M !== 'undefined' && M.toast) {
        M.toast({ html: 'Could not copy table', displayLength: 2000 });
      }
    });
  });
}

if (typeof window !== 'undefined') {
  window.decodeClipboard = { escapeHtml: escapeHtml, cellText: cellText, tableToTsv: tableToTsv, tableToHtml: tableToHtml, attachCopyTableButton: attachCopyTableButton };
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { escapeHtml: escapeHtml, cellText: cellText, tableToTsv: tableToTsv, tableToHtml: tableToHtml, attachCopyTableButton: attachCopyTableButton };
}
