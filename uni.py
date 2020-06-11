from .mappings import bidi, category
import unicodedata as ud


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