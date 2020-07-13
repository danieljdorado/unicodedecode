"""Views."""

from django.shortcuts import render
from Search.forms import UnicodeTextForm
import Search.unicode_util as u


def search(request):
    """Home and search."""
    if request.method == 'POST':
        form = UnicodeTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            normalization_form = u.get_normalization_form(text)
            text = u.examen_unicode(text)
            return render(request, 'search.html', {'form': form,
                                                   'text': text,
                                                   'normalization_form': normalization_form,
                                                   'title': 'Unicode Decode',
                                                   'tagline': 'Decode a Unicode String'})
    form = UnicodeTextForm()
    return render(request, 'home.html', {'form': form})


def tofu(request):
    """Tofu page."""
    return render(request, 'tofu.html', {'title' : 'Tofu',
                                         'tagline' : 'Not Just For Eating'})

def about(request):
    """About Page."""
    return render(request, 'about.html', {'title' : 'About',
                                          'tagline' : 'Get To Know Us'})

def terms(request):
        """Terms and Conditions Page."""
        return render(request, 'terms.html', {'title' : 'Terms and Conditions',
                                              'tagline' : 'User Agreements'})


def character(request, slug):
    """Character page."""

    char = chr(int(slug, 16))
    char_desc = u.get_character_page_description(char)
    return render(request, 'character.html', char_desc)

