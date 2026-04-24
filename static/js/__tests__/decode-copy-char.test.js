/**
 * Unit tests for decode-copy-char.js: attachCopyCharHandler.
 * Clicking a table row copies that row's character (data-char) to the clipboard.
 */

const { attachCopyCharHandler } = require('../decode-copy-char.js');

function tableWithRow(dataChar) {
  var table = document.createElement('table');
  var tbody = document.createElement('tbody');
  var tr = document.createElement('tr');
  if (dataChar !== undefined) tr.setAttribute('data-char', dataChar);
  var td = document.createElement('td');
  td.textContent = dataChar != null ? dataChar : '';
  tr.appendChild(td);
  tbody.appendChild(tr);
  table.appendChild(tbody);
  return { table: table, row: tr };
}

describe('attachCopyCharHandler', () => {
  it('does nothing when table is null', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    expect(() => attachCopyCharHandler(null, clipboard)).not.toThrow();
    expect(clipboard.writeText).not.toHaveBeenCalled();
  });

  it('copies data-char to clipboard when row is clicked', (done) => {
    var _resolve;
    var writePromise = new Promise(function(resolve) { _resolve = resolve; });
    var clipboard = { writeText: jest.fn().mockReturnValue(writePromise) };
    var { table, row } = tableWithRow('A');
    attachCopyCharHandler(table, clipboard);

    row.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).toHaveBeenCalledTimes(1);
    expect(clipboard.writeText).toHaveBeenCalledWith('A');
    _resolve();
    writePromise.then(() => done()).catch(done);
  });

  it('copies when click is on a cell in the row', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    var { table, row } = tableWithRow('B');
    var cell = row.querySelector('td');
    attachCopyCharHandler(table, clipboard);

    cell.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).toHaveBeenCalledWith('B');
  });

  it('copies multi-codepoint character when data-char is emoji', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    var emoji = '\uD83D\uDE00';
    var { table, row } = tableWithRow(emoji);
    attachCopyCharHandler(table, clipboard);

    row.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).toHaveBeenCalledWith(emoji);
  });

  it('does not copy when click is on a link', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    var { table, row } = tableWithRow('X');
    var link = document.createElement('a');
    link.href = '/codepoint/0058';
    link.textContent = 'LATIN X';
    var td = document.createElement('td');
    td.appendChild(link);
    row.appendChild(td);
    attachCopyCharHandler(table, clipboard);

    link.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).not.toHaveBeenCalled();
  });

  it('does not call writeText when row has no data-char attribute', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    var { table, row } = tableWithRow(undefined);
    attachCopyCharHandler(table, clipboard);

    row.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).not.toHaveBeenCalled();
  });

  it('does not throw when clipboard.writeText rejects', (done) => {
    var clipboard = { writeText: jest.fn().mockRejectedValue(new Error('clipboard denied')) };
    var { table, row } = tableWithRow('C');
    attachCopyCharHandler(table, clipboard);

    row.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    setTimeout(done, 0);
  });
});
