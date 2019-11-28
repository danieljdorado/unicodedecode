from django.shortcuts import render
from django.http import HttpResponse
from .forms import UnicodeTextForm
import unicodedata as ud
from .mappings import bidi,category

def search(request):

    if request.method == 'POST':
        form = UnicodeTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            text = examen_unicode(text)
            return render(request, 'search_results.html', {'form': form, 'text': text, 'version': ud.unidata_version})

    form = UnicodeTextForm()
    return render(request, 'base.html', {'form': form})


def examen_unicode(text):
    char_list = []
    for char in text:
        if ord(char) == 0xa:
            # If character is a LINE FEED.

            char_dict = {
            'char': char,
            'name': 'LINE FEED',
            'category': category[ud.category(char)],
            'decimal': '',
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
            'decimal': '',
            'digit': '',
            'bidi': '',
            'ord': ord(char),
            'code_point': 'U+' + str(hex(ord(char))),
            }
            char_list.append(char_dict)
        elif ord(char) == 0x20:
            # If character is SPACE.
            
            print('Carrage return')
            char_dict = {
            'char': char,
            'name': 'SPACE',
            'category': category[ud.category(char)],
            'decimal': '',
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
                'decimal': ud.decimal(char, ''),
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
                'decimal': '',
                'digit': '',
                'bidi': '',
                'ord': ord(char),
                'code_point': 'U+' + str(hex(ord(char))),
                }
                char_list.append(char_dict)

    return char_list
