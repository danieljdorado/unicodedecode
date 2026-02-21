"""Extensions of unicodedata.

Utilities for inspecting Unicode characters: names, categories, normalization,
bidirectional class, East Asian width, and aliases from the Unicode database.
"""

import os
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import unicodedata2 as ud
from decode.mappings import bidi, category, east_asian_categories

# App package directory (decode/)
_APP_DIR: str = os.path.dirname(os.path.abspath(__file__))


class NormalizationForm(str, Enum):
    """Unicode normalization form."""

    NFC = 'NFC'
    NFKC = 'NFKC'
    NFD = 'NFD'
    NFKD = 'NFKD'


@dataclass
class CharacterInfo:
    """Per-character Unicode attributes from examen_unicode."""

    char: str
    name: str
    category: str
    digit: Optional[int]
    bidi: Optional[str]
    ordinal: int
    code_point: str
    hex_code: str


def examen_unicode(text: str) -> List[CharacterInfo]:
    """Build a list of per-character attribute objects for the given text.

    Args:
        text: String of Unicode characters to inspect.

    Returns:
        List of CharacterInfo, one per character.
    """
    return [
        CharacterInfo(
            char=char,
            name=get_name(char),
            category=get_category(char),
            digit=get_digit(char),
            bidi=get_direction(char),
            ordinal=ord(char),
            code_point=get_code_point(char),
            hex_code=get_code_point(char, False),
        )
        for char in text
    ]



def is_normalized(form: NormalizationForm, s: str) -> bool:
    """Return whether the string is already in the given normalization form.

    Args:
        form: Unicode normalization form (NFC, NFKC, NFD, or NFKD).
        s: Unicode string to check.

    Returns:
        True if s is normalized in that form, False otherwise.
    """
    return s == ud.normalize(form.value, s)


def get_normalization_form(string: str) -> Dict[NormalizationForm, bool]:
    """Report which Unicode normalization forms the string is already in.

    Args:
        string: Unicode string to check.

    Returns:
        Dict mapping each normalization form to True if the string is
        normalized in that form, else False.
    """
    normalization_form: Dict[NormalizationForm, bool] = {}
    for form in NormalizationForm:
        normalization_form[form.name] = is_normalized(form, string)
    return normalization_form


def get_code_point(char: str, prefix: bool = True) -> str:
    """Format the character's code point as hex.

    Args:
        char: Single Unicode character (must be length 1).
        prefix: If True, include 'U+' prefix (e.g. 'U+0061'); else bare hex.

    Returns:
        Code point as string, e.g. 'U+0061' or '0061'.

    Raises:
        ValueError: If char is not exactly one character.
    """
    if len(char) != 1:
        raise ValueError(f"get_code_point expects a single character, got length {len(char)}")
    if prefix:
        return f'U+{ord(char):04X}'
    return f'{ord(char):04X}'


class Alias:
    """Look up formal name aliases for Unicode characters from NameAliases.txt."""

    raw: str

    def __init__(self) -> None:
        """Load NameAliases.txt from the package files directory."""
        with open(os.path.join(_APP_DIR, 'files', 'NameAliases.txt'), encoding='utf-8') as f:
            self.raw = f.read()

    def get_aliases(self, char: str) -> List[str]:
        """Return formal name aliases for the character.

        Args:
            char: Single Unicode character.

        Returns:
            List of alias strings.
        """
        code_point: str = get_code_point(char, False)
        pattern: str = f'{code_point};([A-Z ]+);'
        return re.findall(pattern, self.raw, re.IGNORECASE)

    def get_alias(self, char: str) -> str:
        """Return the first formal name alias for the character, or 'UNKNOWN'.

        Args:
            char: Single Unicode character.

        Returns:
            First alias string, or 'UNKNOWN' if none are found.
        """
        aliases: List[str] = self.get_aliases(char)

        if aliases:
            return aliases[0]
        return "UNKNOWN"


alias: Alias = Alias()


def get_name(char: str) -> str:
    """Return the Unicode character name, or first alias if no name is defined.

    Args:
        char: Single Unicode character.

    Returns:
        Official name or first alias string.
    """
    try:
        name: str = ud.name(char)
    except ValueError:
        name = alias.get_alias(char)
    return name

def get_category(char: str) -> str:
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


def get_digit(char: str) -> Optional[int]:
    """Return the digit value for numeric characters.

    Args:
        char: Single Unicode character.

    Returns:
        Digit value (e.g. 0-9 for decimal digits), or None if not a digit.
    """
    try:
        return ud.digit(char)
    except (ValueError, TypeError):
        return None


def get_direction(char: str) -> Optional[str]:
    """Return the character's bidirectional class label.

    Args:
        char: Single Unicode character.

    Returns:
        Bidi class string (e.g. 'LEFT-TO-RIGHT'), or None if not in our mapping.
    """
    try:
        return bidi[ud.bidirectional(char)]
    except KeyError:
        return None


def get_east_asian_width(char: str) -> Optional[str]:
    """Return the East Asian width category for the character.

    Args:
        char: Single Unicode character.

    Returns:
        Width label (e.g. 'East Asian Fullwidth') or raw property value,
        or None on invalid input.
    """
    try:
        width: str = ud.east_asian_width(char)
        return east_asian_categories.get(width, width)
    except (ValueError, TypeError):
        return None

@dataclass
class CodepointDescription:
    """Character attributes for the codepoint detail page."""

    title: str
    tagline: str
    char: str
    name: str
    category: str
    digit: Optional[int]
    direction: Optional[str]
    integer: int
    upper: str
    lower: str
    decomposition: str
    aliases: str
    east_asian: Optional[str]


def get_character_page_description(char: str) -> CodepointDescription:
    """Build character attributes for a detail/codepoint page.

    Args:
        char: Single Unicode character.

    Returns:
        CodepointDescription with all fields for the codepoint template.
    """
    return CodepointDescription(
        title=get_name(char),
        tagline=get_code_point(char),
        char=char,
        name=get_name(char),
        category=get_category(char),
        digit=get_digit(char),
        direction=get_direction(char),
        integer=ord(char),
        upper=char.upper(),
        lower=char.lower(),
        decomposition=ud.decomposition(char),
        aliases=', '.join(alias.get_aliases(char)),
        east_asian=get_east_asian_width(char),
    )
