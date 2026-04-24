/**
 * Unit tests for codepoint-go-back.js: shouldShowGoBack and hideGoBackIfNoHistory.
 */

const { shouldShowGoBack, hideGoBackIfNoHistory } = require('../codepoint-go-back.js');

describe('shouldShowGoBack', () => {
  const originalHistory = window.history;

  afterEach(() => {
    Object.defineProperty(window, 'history', { value: originalHistory, configurable: true });
  });

  it('returns false when history.length is 1', () => {
    Object.defineProperty(window, 'history', { value: { length: 1 }, configurable: true });
    expect(shouldShowGoBack()).toBe(false);
  });

  it('returns false when history.length is 0', () => {
    Object.defineProperty(window, 'history', { value: { length: 0 }, configurable: true });
    expect(shouldShowGoBack()).toBe(false);
  });

  it('returns true when history.length is 2', () => {
    Object.defineProperty(window, 'history', { value: { length: 2 }, configurable: true });
    expect(shouldShowGoBack()).toBe(true);
  });

  it('returns true when history.length is greater than 2', () => {
    Object.defineProperty(window, 'history', { value: { length: 5 }, configurable: true });
    expect(shouldShowGoBack()).toBe(true);
  });

  it('returns false when history is null', () => {
    Object.defineProperty(window, 'history', { value: null, configurable: true });
    expect(shouldShowGoBack()).toBe(false);
  });
});

describe('hideGoBackIfNoHistory', () => {
  const originalHistory = window.history;

  beforeEach(() => {
    document.body.innerHTML = '<div id="go-back-container"><a href="#">Go Back</a></div>';
  });

  afterEach(() => {
    document.body.innerHTML = '';
    Object.defineProperty(window, 'history', { value: originalHistory, configurable: true });
  });

  it('hides go-back-container when history.length is 1', () => {
    Object.defineProperty(window, 'history', { value: { length: 1 }, configurable: true });
    const el = document.getElementById('go-back-container');
    expect(el.style.display).toBe('');
    hideGoBackIfNoHistory();
    expect(el.style.display).toBe('none');
  });

  it('does not hide go-back-container when history.length is 2', () => {
    Object.defineProperty(window, 'history', { value: { length: 2 }, configurable: true });
    const el = document.getElementById('go-back-container');
    hideGoBackIfNoHistory();
    expect(el.style.display).toBe('');
  });

  it('does nothing when go-back-container is missing', () => {
    document.body.innerHTML = '';
    Object.defineProperty(window, 'history', { value: { length: 1 }, configurable: true });
    expect(() => hideGoBackIfNoHistory()).not.toThrow();
  });
});
