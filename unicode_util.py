"""Extensions of unicodedata.

Utilities for inspecting Unicode characters: names, categories, normalization,
bidirectional class, East Asian width, and aliases from the Unicode database.
"""

import os
import re
import unicodedata as ud
from decode.mappings import bidi, category, east_asian_categories

# App package directory (decode/)
_APP_DIR = os.path.dirname(os.path.abspath(__file__))

def examen_unicode(text):
    """Build a list of per-character attribute dicts for the given text.

    Args:
        text: String of Unicode characters to inspect.

    Returns:
        List of dicts, one per character, with keys such as 'char', 'name',
        'category', 'digit', 'bidi', 'ord', 'code_point', and 'hex'.
    """
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
    """Report which Unicode normalization forms the string is already in.

    Args:
        string: Unicode string to check.

    Returns:
        Dict mapping form name ('NFC', 'NFKC', 'NFD', 'NFKD') to True if
        the string is normalized in that form, else False.
    """
    forms = ['NFC', 'NFKC', 'NFD', 'NFKD']
    normalization_form = {}

    for form in forms:
        if ud.is_normalized(form, string):
            normalization_form[form] = True
        else:
            normalization_form[form] = False
    return normalization_form


def get_code_point(char, prefix=True):
    """Format the character's code point as hex.

    Args:
        char: Single Unicode character.
        prefix: If True, include 'U+' prefix (e.g. 'U+0061'); else bare hex.

    Returns:
        Code point as string, e.g. 'U+0061' or '0061'.
    """
    if prefix:
        return f'U+{ord(char):04X}'
    return f'{ord(char):04X}'


class Alias:
    """Look up formal name aliases for Unicode characters from NameAliases.txt."""

    def __init__(self):
        """Load NameAliases.txt from the package files directory."""
        with open(os.path.join(_APP_DIR, 'files', 'NameAliases.txt'), encoding='utf-8') as f:
            self.raw = f.read()


    def get_aliases(self, char, format=False):
        """Return formal name aliases for the character.

        Args:
            char: Single Unicode character.
            format: If True, return a single comma-separated string; else list.

        Returns:
            List of alias strings, or comma-separated string if format is True.
        """
        code_point = get_code_point(char, False)
        pattern = f'{code_point};([A-Z ]+);'
        aliases = re.findall(pattern, self.raw, re.IGNORECASE)

        if format:
            return ', '.join(aliases)
        return aliases

    def get_alias(self, char):
        """Return the first formal name alias for the character, or 'UNKNOWN'.

        Args:
            char: Single Unicode character.

        Returns:
            First alias string, or 'UNKNOWN' if none are found.
        """
        aliases = self.get_aliases(char)

        if aliases:
            return aliases[0]
        return "UNKNOWN"


alias = Alias()


def get_name(char):
    """Return the Unicode character name, or first alias if no name is defined.

    Args:
        char: Single Unicode character.

    Returns:
        Official name or first alias string.
    """
    try:
        name = ud.name(char)
    except ValueError:
        name = alias.get_alias(char)
    return name

def get_category(char):
    """Return a human-readable character general category.

    Args:
        char: Single Unicode character.

    Returns:
        Category label string (e.g. 'UPPERCASE LETTER'), or '' if unknown.
    """
    try:
        return category[ud.category(char)]
    except KeyError:
        return ''


def get_digit(char):
    """Return the digit value for numeric characters.

    Args:
        char: Single Unicode character.

    Returns:
        Digit value (e.g. 0-9 for decimal digits), or '' if not a digit.
    """
    try:
        return ud.digit(char, '')
    except (ValueError, TypeError):
        return ''


def get_direction(char):
    """Return the character's bidirectional class label.

    Args:
        char: Single Unicode character.

    Returns:
        Bidi class string (e.g. 'LEFT-TO-RIGHT'), or '' if not in our mapping.
    """
    try:
        return bidi[ud.bidirectional(char)]
    except KeyError:
        return ''


def get_east_asian_width(char):
    """Return the East Asian width category for the character.

    Args:
        char: Single Unicode character.

    Returns:
        Width label (e.g. 'East Asian Fullwidth') or raw property value,
        or '' on invalid input.
    """
    try:
        width = ud.east_asian_width(char)
        return east_asian_categories.get(width, width)
    except (ValueError, TypeError):
        return ''

def get_character_page_description(char):
    """Build a dict of character attributes for a detail/codepoint page.

    Args:
        char: Single Unicode character.

    Returns:
        Dict with 'title', 'tagline', 'char', 'name', 'category', 'digit',
        'direction', 'integer', 'upper', 'lower', 'decomposition', 'aliases',
        and 'east_asian'.
    """
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
