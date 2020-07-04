"""Extensions of unicodedata."""

import unicodedata as ud
from Search.mappings import bidi, category


def examen_unicode(text):
    """Returns a list of dictionaries for each unicode character."""

    char_list = []
    for char in text:
        char_dict = {
            'char' : char,
            'name' : get_name(char),
            'category' : get_category(char),
            'digit' : get_digit(char),
            'bidi' : get_direction(char),
            'ord' : ord(char),
            'code_point' : get_code_point(char),
            'hex' : get_code_point(char, False),
        }

        char_list.append(char_dict)
    return char_list


def get_normalization_form(string):
    """Return Dictionary of Normalization Forms."""

    forms = ['NFC', 'NFKC', 'NFD', 'NFKD']
    normalization_form = dict()

    for form in forms:
        if ud.is_normalized(form, string):
            normalization_form[form] = True
        else:
            normalization_form[form] = False
    return normalization_form


UNICODE_ALIASES = {
    'U+000A' : 'LINE FEED',
    'U+000D' : 'CARRIAGE RETURN',
    'U+0020' : 'SPACE',
}

def get_code_point(char, prefix=True):
    """Return character codepoint."""
    if prefix:
        return 'U+{:04X}'.format(ord(char))
    return '{:04X}'.format(ord(char))


def get_name(char):
    """Return Unicode character name or alias"""
    code_point = get_code_point(char)
    if code_point in UNICODE_ALIASES:
        return UNICODE_ALIASES[code_point]
    try:
        return ud.name(char)
    except: # pylint: disable=bare-except
        return 'UNKNOWN'

def get_category(char):
    """Return character category."""
    try:
        return category[ud.category(char)]
    except: # pylint: disable=bare-except
        return ''


def get_digit(char):
    """Return character digit."""
    try:
        return ud.digit(char, '')
    except: # pylint: disable=bare-except
        return ''


def get_direction(char):
    """Return character direction."""
    try:
        return bidi[ud.bidirectional(char)]
    except: # pylint: disable=bare-except
        return ''

def get_character_page_description(char):
    """Return dictionary of character attributes"""
    return {
        'title' : get_name(char),
        'tagline' : get_code_point(char),
        'char' : char,
        'name' : get_name(char),
        'category' : get_category(char),
        'digit': get_digit(char),
        'direction': get_direction(char),
    }
