/**
 * Unit tests for decode-live.js live update behavior.
 */

function flushPromises() {
  return new Promise(function(resolve) {
    setTimeout(resolve, 0);
  });
}

function setupDom() {
  document.body.innerHTML = [
    '<form action="/" method="post">',
    '<input type="hidden" name="csrfmiddlewaretoken" value="token-123">',
    '<textarea id="textarea1" class="materialize-textarea"></textarea>',
    '<button id="decode-button" type="submit">Examine</button>',
    '<button id="share-button" type="button">Share</button>',
    '</form>',
    '<div id="decode-results-container"></div>',
    '<div id="home-features"></div>',
  ].join('');
}

describe('decode-live', function() {
  beforeEach(function() {
    jest.resetModules();
    setupDom();
  });

  afterEach(function() {
    document.body.innerHTML = '';
    delete global.fetch;
  });

  it('posts exact text including boundary whitespace', async function() {
    var fetchMock = jest.fn().mockResolvedValue({
      text: function() { return Promise.resolve('<div id="codepoint-details-table"></div>'); }
    });
    global.fetch = fetchMock;
    require('../decode-live.js');

    var textarea = document.getElementById('textarea1');
    textarea.value = '  ab  ';
    textarea.dispatchEvent(new Event('input', { bubbles: true }));

    await new Promise(function(resolve) { setTimeout(resolve, 380); });
    await flushPromises();

    expect(fetchMock).toHaveBeenCalledTimes(1);
    var call = fetchMock.mock.calls[0];
    expect(call[1].method).toBe('POST');
    expect(call[1].body).toContain('text=++ab++');
    expect(call[1].headers['X-Decode-Live']).toBe('1');
  });

  it('ignores stale responses from older requests', async function() {
    var resolvers = [];
    global.fetch = jest.fn().mockImplementation(function() {
      return new Promise(function(resolve) {
        resolvers.push(resolve);
      });
    });
    require('../decode-live.js');

    var textarea = document.getElementById('textarea1');
    var container = document.getElementById('decode-results-container');

    textarea.value = 'first';
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    await new Promise(function(resolve) { setTimeout(resolve, 380); });

    textarea.value = 'second';
    textarea.dispatchEvent(new Event('input', { bubbles: true }));
    await new Promise(function(resolve) { setTimeout(resolve, 380); });

    resolvers[1]({
      text: function() { return Promise.resolve('SECOND_RESULT'); }
    });
    await flushPromises();
    expect(container.innerHTML).toBe('SECOND_RESULT');

    resolvers[0]({
      text: function() { return Promise.resolve('FIRST_RESULT'); }
    });
    await flushPromises();
    expect(container.innerHTML).toBe('SECOND_RESULT');
  });
});
