"""Unicode decode app views.

Handles rendering of the about, codepoint, decode, privacy, terms, and tofu
pages, and processes Unicode text decoding form submissions.
"""

from collections import Counter
from dataclasses import asdict
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from decode.forms import UnicodeTextForm
from decode.mappings import INVISIBLE_CHARACTERS
import decode.unicode_util as u

# Short descriptions for normalization form column tooltips.
NORMALIZATION_DESCRIPTIONS = {
    u.NormalizationForm.NFC: 'Canonical Composition: precomposed characters where possible (e.g. é as single character).',
    u.NormalizationForm.NFD: 'Canonical Decomposition: split into base character + combining marks (e.g. e + ´).',
    u.NormalizationForm.NFKC: 'Compatibility Composition: precomposed + compatibility equivalents (e.g. ﬁ → fi).',
    u.NormalizationForm.NFKD: 'Compatibility Decomposition: decomposed + compatibility equivalents.',
}


def _normalization_form_with_descriptions(normalization_form):
    """Return a list of (form, value, description) for the normalization table and tooltips."""
    return [
        (form, normalization_form[form], NORMALIZATION_DESCRIPTIONS[form])
        for form in u.NormalizationForm
    ]


def _text_summary(text):
    """Build summary dict from decoded text (list of CharacterInfo): num_chars, num_bytes, num_tokens, top3."""
    if not text:
        return {
            'num_chars': 0,
            'num_bytes': 0,
            'num_tokens': 0,
            'top3': [],
        }
    num_chars = len(text)
    num_bytes = sum(len(info.char.encode('utf-8')) for info in text)
    num_tokens = len(''.join(info.char for info in text).split())
    counts = Counter(info.char for info in text)
    top3 = []
    for c, n in counts.most_common(3):
        code_point = u.get_code_point(c)
        if c == ' ':
            display = 'space'
        elif ord(c) in INVISIBLE_CHARACTERS:
            display = INVISIBLE_CHARACTERS[ord(c)]
        else:
            display = c
        top3.append({'char': c, 'count': n, 'code_point': code_point, 'display': display})
    return {
        'num_chars': num_chars,
        'num_bytes': num_bytes,
        'num_tokens': num_tokens,
        'top3': top3,
    }


def _decode_context(form, raw_text):
    """Build common context used by decode result renders."""
    normalization_form = u.get_normalization_form(raw_text)
    normalization_form_list = _normalization_form_with_descriptions(normalization_form)
    text = u.examen_unicode(raw_text)
    summary = _text_summary(text)
    return {
        'form': form,
        'text': text,
        'summary': summary,
        'normalization_form': normalization_form,
        'normalization_form_list': normalization_form_list,
        'title': 'Unicode Decode',
        'tagline': 'See every character behind your text instantly',
    }


def about(request):
    """Render the About page.

    Returns:
        HttpResponse: Rendered about.html with title and tagline context.
    """
    return render(request, 'decode/about.html', {'title' : 'About',
                                         'tagline' : 'Get To Know Us'})


def codepoint(request, slug):
    """Render the codepoint detail page for a Unicode code point.

    Args:
        request: The HTTP request.
        slug: Hex string of the Unicode code point (e.g. '0041' for 'A').

    Returns:
        HttpResponse: Rendered codepoint.html with codepoint description context.
    """
    char = chr(int(slug, 16))
    char_desc = u.get_character_page_description(char)
    return render(request, 'decode/codepoint.html', asdict(char_desc))


def privacy(request):
    """Render the Privacy Policy page.

    Returns:
        HttpResponse: Rendered privacy.html with title and tagline context.
    """
    return render(request, 'decode/privacy.html', {'title' : 'Privacy Policy',
                                              'tagline' : "We're Not Tracking"})


def decode(request):
    """Handle the decode page: show form on GET, decode Unicode text on POST.

    GET returns the home form, or decode results if the `s` query parameter
    is present (e.g. /?s=abcd). POST validates the form, normalizes and analyzes
    the submitted text, then renders the decode results.

    Returns:
        HttpResponse: Rendered home.html (GET) or decode.html (POST) with form
            and optionally decoded text and normalization form context.
    """
    if request.method == 'POST':
        form = UnicodeTextForm(request.POST)
        if form.is_valid():
            raw_text = form.cleaned_data['text']
            context = _decode_context(form, raw_text)
            if request.headers.get('X-Decode-Live') == '1':
                html = render_to_string('decode/_decode_results.html', context, request=request)
                return HttpResponse(html)
            return render(request, 'decode/decode.html', context)

    # GET with ?s=... : show decode results for that string
    query_string = request.GET.get('s')
    if query_string is not None and query_string != '':
        form = UnicodeTextForm(initial={'text': query_string})
        return render(request, 'decode/decode.html', _decode_context(form, query_string))

    form = UnicodeTextForm()
    return render(request, 'decode/home.html', {'form': form})


def terms(request):
    """Render the Terms and Conditions page.

    Returns:
        HttpResponse: Rendered terms.html with title and tagline context.
    """
    return render(request, 'decode/terms.html', {'title' : 'Terms and Conditions',
                                              'tagline' : 'User Agreements'})


def tofu(request):
    """Render the Tofu (missing glyphs) information page.

    Returns:
        HttpResponse: Rendered tofu.html with title and tagline context.
    """
    return render(request, 'decode/tofu.html', {'title' : 'Tofu',
                                         'tagline' : 'Not Just For Eating'})
