/**
 * Unit tests for decode-copy-char.js: attachCopyCharHandler.
 */

const { attachCopyCharHandler } = require('../decode-copy-char.js');

function tableWithCopyButton(dataChar) {
  var table = document.createElement('table');
  var tbody = document.createElement('tbody');
  var tr = document.createElement('tr');
  var td = document.createElement('td');
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'copy-char-btn';
  if (dataChar !== undefined) btn.setAttribute('data-char', dataChar);
  btn.innerHTML = '<i class="material-icons">content_copy</i>';
  td.appendChild(btn);
  tr.appendChild(td);
  tbody.appendChild(tr);
  table.appendChild(tbody);
  return { table: table, btn: btn };
}

describe('attachCopyCharHandler', () => {
  it('does nothing when table is null', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    expect(() => attachCopyCharHandler(null, clipboard)).not.toThrow();
    expect(clipboard.writeText).not.toHaveBeenCalled();
  });

  it('copies data-char to clipboard when copy button is clicked', (done) => {
    var _resolve;
    var writePromise = new Promise(function(resolve) { _resolve = resolve; });
    var clipboard = { writeText: jest.fn().mockReturnValue(writePromise) };
    var { table, btn } = tableWithCopyButton('A');
    attachCopyCharHandler(table, clipboard);

    btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).toHaveBeenCalledTimes(1);
    expect(clipboard.writeText).toHaveBeenCalledWith('A');
    _resolve();
    writePromise.then(() => done()).catch(done);
  });

  it('copies multi-codepoint character when data-char is emoji', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    var emoji = '\uD83D\uDE00';
    var { table, btn } = tableWithCopyButton(emoji);
    attachCopyCharHandler(table, clipboard);

    btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).toHaveBeenCalledWith(emoji);
  });

  it('does not call writeText when click target is not the copy button', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    var { table } = tableWithCopyButton('X');
    var otherCell = document.createElement('td');
    otherCell.textContent = 'other';
    table.querySelector('tr').appendChild(otherCell);
    attachCopyCharHandler(table, clipboard);

    otherCell.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).not.toHaveBeenCalled();
  });

  it('does not call writeText when button has no data-char attribute', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    var { table, btn } = tableWithCopyButton(undefined);
    attachCopyCharHandler(table, clipboard);

    btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).not.toHaveBeenCalled();
  });

  it('calls writeText when click is on the icon inside the button (event delegation)', () => {
    var clipboard = { writeText: jest.fn().mockResolvedValue(undefined) };
    var { table, btn } = tableWithCopyButton('B');
    var icon = btn.querySelector('i');
    attachCopyCharHandler(table, clipboard);

    icon.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    expect(clipboard.writeText).toHaveBeenCalledWith('B');
  });

  it('does not throw when clipboard.writeText rejects', (done) => {
    var clipboard = { writeText: jest.fn().mockRejectedValue(new Error('clipboard denied')) };
    var { table, btn } = tableWithCopyButton('C');
    attachCopyCharHandler(table, clipboard);

    btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));

    setTimeout(done, 0);
  });
});
