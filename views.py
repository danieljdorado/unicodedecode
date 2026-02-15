"""Views."""

from django.shortcuts import render
from unicodedecode.forms import UnicodeTextForm
import unicodedecode.unicode_util as u


def about(request):
    """About Page."""
    return render(request, 'decode/about.html', {'title' : 'About',
                                         'tagline' : 'Get To Know Us'})


def character(request, slug):
    """Character page."""

    char = chr(int(slug, 16))
    char_desc = u.get_character_page_description(char)
    return render(request, 'decode/character.html', char_desc)

def privacy(request):
        """Terms and Conditions Page."""
        return render(request, 'decode/privacy.html', {'title' : 'Privacy Policy',
                                              'tagline' : "We're Not Tracking"})


def decode(request):
    """Home and decode."""
    if request.method == 'POST':
        form = UnicodeTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            normalization_form = u.get_normalization_form(text)
            text = u.examen_unicode(text)
            return render(request, 'decode/decode.html', {'form': form,
                                                   'text': text,
                                                   'normalization_form': normalization_form,
                                                   'title' : 'Unicode Decode',
                                                   'tagline' : 'Decode a Unicode String'})

    form = UnicodeTextForm()
    return render(request, 'decode/home.html', {'form': form})


def terms(request):
        """Terms and Conditions Page."""
        return render(request, 'decode/terms.html', {'title' : 'Terms and Conditions',
                                              'tagline' : 'User Agreements'})


def tofu(request):
    """Tofu page."""
    return render(request, 'decode/tofu.html', {'title' : 'Tofu',
                                         'tagline' : 'Not Just For Eating'})
