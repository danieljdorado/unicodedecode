"""Unicode decode app views.

Handles rendering of the about, codepoint, decode, privacy, terms, and tofu
pages, and processes Unicode text decoding form submissions.
"""

from dataclasses import asdict
from django.shortcuts import render
from decode.forms import UnicodeTextForm
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
            text = form.cleaned_data['text']
            normalization_form = u.get_normalization_form(text)
            normalization_form_list = _normalization_form_with_descriptions(normalization_form)
            text = u.examen_unicode(text)
            return render(request, 'decode/decode.html', {'form': form,
                                                   'text': text,
                                                   'normalization_form': normalization_form,
                                                   'normalization_form_list': normalization_form_list,
                                                   'title' : 'Unicode Decode',
                                                   'tagline' : 'See every character behind your text instantly'})

    # GET with ?s=... : show decode results for that string
    query_string = request.GET.get('s', '').strip()
    if query_string:
        form = UnicodeTextForm(initial={'text': query_string})
        normalization_form = u.get_normalization_form(query_string)
        normalization_form_list = _normalization_form_with_descriptions(normalization_form)
        text = u.examen_unicode(query_string)
        return render(request, 'decode/decode.html', {'form': form,
                                               'text': text,
                                               'normalization_form': normalization_form,
                                               'normalization_form_list': normalization_form_list,
                                               'title': 'Unicode Decode',
                                               'tagline': 'See every character behind your text instantly'})

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
