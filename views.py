from django.shortcuts import render
from django.http import HttpResponse
from .forms import UnicodeTextForm
import unicodedata as ud
from .mappings import bidi,category

def search(request):
    """View for home page and search."""
    if request.method == 'POST':
        form = UnicodeTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            normalization_form = get_normalization_form(text)
            text = examen_unicode(text)
            return render(request, 'search_results.html', {'form': form,
                                                            'text': text,
                                                            'version': ud.unidata_version,
                                                            'normalization_form': normalization_form,})
    form = UnicodeTextForm()
    return render(request, 'search_base.html', {'form': form})


def examen_unicode(text):
    """Returns a list of dictionaries for each unicode character."""
    char_list = []
    for char in text:
        if ord(char) == 0xa:
            # If character is a LINE FEED.
            char_dict = {
            'char': char,
            'name': 'LINE FEED',
            'category': category[ud.category(char)],
            'digit': '',
            'bidi': '',
            'ord': ord(char),
            'code_point': 'U+' + str(hex(ord(char))),
            }
            char_list.append(char_dict)

        elif ord(char) == 0xd:
            # If character is a Carriage Return.
            char_dict = {
            'char': char,
            'name': 'CARRIAGE RETURN',
            'category': category[ud.category(char)],
            'digit': '',
            'bidi': '',
            'ord': ord(char),
            'code_point': 'U+' + str(hex(ord(char))),
            }
            char_list.append(char_dict)
        elif ord(char) == 0x20:
            # If character is SPACE.
            char_dict = {
            'char': char,
            'name': 'SPACE',
            'category': category[ud.category(char)],
            'digit': '',
            'bidi': '',
            'ord': ord(char),
            'code_point': 'U+' + str(hex(ord(char))),
            }
            char_list.append(char_dict)
        else:
            # Default.
            try:
                char_dict = {
                'char': char,
                'name': ud.name(char),
                'category': category[ud.category(char)],
                'digit': ud.digit(char, ''),
                'bidi': bidi[ud.bidirectional(char)],
                'ord': ord(char),
                'code_point': 'U+' + str(hex(ord(char))),
                }
                char_list.append(char_dict)
            except:
                char_dict = {
                'char': char,
                'name': 'UNKNOWN',
                'category': '',
                'digit': '',
                'bidi': '',
                'ord': ord(char),
                'code_point': 'U+' + str(hex(ord(char))),
                }
                char_list.append(char_dict)

    return char_list

def get_normalization_form(string):
    """Return Dictionary of Normalization Forms"""

    normalization_form = {
        'NFC': False,
        'NFKC': False,
        'NFD': False,
        'NFKD': False,
    }

    for form in normalization_form:
        if ud.is_normalized(form, string) == True:
            normalization_form[form] = True
    return normalization_form

def tofu(request):
    'View for tofu page.'
    return render(request, 'tofu.html', {'title' : 'Tofu',
                                         'tagline' : 'Not just for eating'})
