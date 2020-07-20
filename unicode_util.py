"""Extensions of unicodedata."""

import re
import unicodedata as ud
from decode.mappings import bidi, category, east_asian_categories


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


def get_code_point(char, prefix=True):
    """Return character codepoint."""
    if prefix:
        return 'U+{:04X}'.format(ord(char))
    return '{:04X}'.format(ord(char))


class Alias:
    """Class to manipulate aliases"""

    def __init__(self):
        with open('decode/NameAliases.txt') as f:
            self.raw = f.read()


    def get_aliases(self, char, format=False):
        """Return a list of aliases for a character"""

        code_point = get_code_point(char, False)      
        self.pattern = f'{code_point};([A-Z ]+);'
        self.aliases = re.findall(self.pattern, self.raw, re.IGNORECASE)

        if format:
            return ', '.join(self.aliases)
        return self.aliases

    def get_alias(self, char):
        """Return the first alias for a character"""
        
        aliases = self.get_aliases(char)

        if aliases:
            return aliases[0]
        return "UNKNOWN"


alias = Alias()


def get_name(char):
    """Return Unicode character name or alias"""

    try:
        name = ud.name(char)
    except: # pylint: disable=bare-except
        name = alias.get_alias(char)
    return name

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


def get_east_asian_width(char):
    """Return East Asian Width Attribute."""
    try:
        width = ud.east_asian_width(char)
        return east_asian_categories[width]
    except: # pylint: disable=bare-except
        return ud.east_asian_width(char)

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
        'integer': ord(char),
        'upper': char.upper(),
        'lower' : char.lower(),
        'decomposition': ud.decomposition(char),
        'aliases': alias.get_aliases(char, True),
        'east_asian': get_east_asian_width(char),
    }
