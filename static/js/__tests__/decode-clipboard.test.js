/**
 * Unit tests for decode-clipboard.js: escapeHtml, cellText, tableToTsv, tableToHtml.
 */

const { escapeHtml, cellText, tableToTsv, tableToHtml } = require('../decode-clipboard.js');

describe('escapeHtml', () => {
  it('escapes < and >', () => {
    expect(escapeHtml('<script>')).toBe('&lt;script&gt;');
    expect(escapeHtml('a<b>c')).toBe('a&lt;b&gt;c');
  });

  it('escapes &', () => {
    expect(escapeHtml('a & b')).toBe('a &amp; b');
  });

  it('does not escape double quotes (div innerHTML leaves them as-is)', () => {
    expect(escapeHtml('say "hi"')).toBe('say "hi"');
  });

  it('returns empty string for empty input', () => {
    expect(escapeHtml('')).toBe('');
  });

  it('passes through safe text unchanged', () => {
    expect(escapeHtml('LATIN CAPITAL LETTER A')).toBe('LATIN CAPITAL LETTER A');
  });
});

describe('cellText', () => {
  it('returns escaped text when cell has no link', () => {
    const td = document.createElement('td');
    td.textContent = 'Ll';
    expect(cellText(td)).toBe('Ll');
  });

  it('returns escaped text for plain text with special chars', () => {
    const td = document.createElement('td');
    td.textContent = 'N/A';
    expect(cellText(td)).toBe('N/A');
  });

  it('returns anchor HTML when cell contains a link', () => {
    const td = document.createElement('td');
    const a = document.createElement('a');
    a.href = 'http://example.com/codepoint/0041';
    a.textContent = 'LATIN CAPITAL LETTER A';
    td.appendChild(a);
    expect(cellText(td)).toBe(
      '<a href="http://example.com/codepoint/0041">LATIN CAPITAL LETTER A</a>'
    );
  });

  it('escapes link href and text', () => {
    const td = document.createElement('td');
    const a = document.createElement('a');
    a.href = 'http://example.com?a=1&b=2';
    a.textContent = 'A & B';
    td.appendChild(a);
    expect(cellText(td)).toContain('&amp;');
    expect(cellText(td)).toContain('a=1&amp;b=2');
  });
});

describe('tableToTsv', () => {
  it('returns only body rows when table has no thead', () => {
    const table = document.createElement('table');
    const tbody = document.createElement('tbody');
    const tr = document.createElement('tr');
    tr.innerHTML = '<td>a</td>';
    tbody.appendChild(tr);
    table.appendChild(tbody);
    expect(tableToTsv(table)).toBe('a');
  });

  it('returns header row only when tbody is empty', () => {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    thead.innerHTML = '<tr><th>Char</th><th>Name</th></tr>';
    table.appendChild(thead);
    table.appendChild(document.createElement('tbody'));
    expect(tableToTsv(table)).toBe('Char\tName');
  });

  it('returns header and data rows tab-separated', () => {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    thead.innerHTML = '<tr><th>Character</th><th>Name</th></tr>';
    const tbody = document.createElement('tbody');
    const tr = document.createElement('tr');
    tr.innerHTML = '<td>A</td><td><a href="/cp/41">LATIN A</a></td>';
    tbody.appendChild(tr);
    table.appendChild(thead);
    table.appendChild(tbody);
    expect(tableToTsv(table)).toBe('Character\tName\nA\tLATIN A');
  });

  it('uses only text content (strips link markup) in TSV', () => {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    thead.innerHTML = '<tr><th>Name</th></tr>';
    const tbody = document.createElement('tbody');
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    const a = document.createElement('a');
    a.href = 'http://example.com/x';
    a.textContent = 'Link text';
    td.appendChild(a);
    tr.appendChild(td);
    tbody.appendChild(tr);
    table.appendChild(thead);
    table.appendChild(tbody);
    expect(tableToTsv(table)).toBe('Name\nLink text');
  });
});

describe('tableToHtml', () => {
  it('includes meta charset and table structure', () => {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    thead.innerHTML = '<tr><th>X</th></tr>';
    const tbody = document.createElement('tbody');
    table.appendChild(thead);
    table.appendChild(tbody);
    const html = tableToHtml(table);
    expect(html).toMatch(/<meta charset="UTF-8">/);
    expect(html).toMatch(/<table>/);
    expect(html).toMatch(/<thead>/);
    expect(html).toMatch(/<tbody>/);
    expect(html).toMatch(/<th>X<\/th>/);
  });

  it('includes escaped header cells', () => {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tr = document.createElement('tr');
    const th = document.createElement('th');
    th.textContent = 'A & B';
    tr.appendChild(th);
    thead.appendChild(tr);
    table.appendChild(thead);
    table.appendChild(document.createElement('tbody'));
    const html = tableToHtml(table);
    expect(html).toContain('<th>A &amp; B</th>');
  });

  it('preserves links in body cells', () => {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    thead.innerHTML = '<tr><th>Name</th></tr>';
    const tbody = document.createElement('tbody');
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    const a = document.createElement('a');
    a.href = 'http://example.com/codepoint/0041';
    a.textContent = 'LATIN CAPITAL LETTER A';
    td.appendChild(a);
    tr.appendChild(td);
    tbody.appendChild(tr);
    table.appendChild(thead);
    table.appendChild(tbody);
    const html = tableToHtml(table);
    expect(html).toContain('http://example.com/codepoint/0041');
    expect(html).toContain('LATIN CAPITAL LETTER A');
    expect(html).toMatch(/<a href=/);
  });

  it('outputs multiple rows correctly', () => {
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    thead.innerHTML = '<tr><th>Char</th></tr>';
    const tbody = document.createElement('tbody');
    ['A', 'B'].forEach((c) => {
      const tr = document.createElement('tr');
      const td = document.createElement('td');
      td.textContent = c;
      tr.appendChild(td);
      tbody.appendChild(tr);
    });
    table.appendChild(thead);
    table.appendChild(tbody);
    const html = tableToHtml(table);
    expect(html).toContain('<td>A</td>');
    expect(html).toContain('<td>B</td>');
  });
});
