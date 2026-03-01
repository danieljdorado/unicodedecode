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
from decode.mappings import (
    bidi,
    category,
    east_asian_categories,
    name_prefix_to_script,
    script_display,
    is_homoglyph_codepoint,
    INVISIBLE_CHARACTERS,
)

# App package directory (decode/)
_APP_DIR: str = os.path.dirname(os.path.abspath(__file__))


class NormalizationForm(str, Enum):
    """Unicode normalization form."""

    NFC = 'NFC'  # Canonical Composition
    NFKC = 'NFKC'  # Compatibility Composition
    NFD = 'NFD'  # Canonical Decomposition
    NFKD = 'NFKD'  # Compatibility Decomposition


@dataclass
class CharacterInfo:
    """Per-character Unicode attributes from examen_unicode."""

    char: str
    name: str
    category: Optional[str]
    digit: Optional[int]
    bidi: Optional[str]
    ordinal: int
    code_point: str
    hex_code: str
    utf8_bytes: str
    html_entity: str
    script: Optional[str]
    homoglyph_risk: Optional[str]
    invisible: Optional[str]


def get_homoglyph_risk(char: str) -> Optional[str]:
    """Return 'Yes' if the character is commonly used in spoofing/homoglyph attacks, else None."""
    if len(char) != 1:
        return None
    return 'Yes' if is_homoglyph_codepoint(ord(char)) else None


def get_invisible_warning(char: str) -> Optional[str]:
    """Return a short label for invisible/zero-width characters, else None."""
    if len(char) != 1:
        return None
    return INVISIBLE_CHARACTERS.get(ord(char))


def get_script(char: str) -> Optional[str]:
    """Return the Unicode script (e.g. Latin, Cyrillic, Arabic) for homoglyph detection.

    Uses ud.script() when available (e.g. unicodedata2), otherwise infers from
    the character name (e.g. "LATIN CAPITAL LETTER A" -> "Latin").

    Args:
        char: Single Unicode character.

    Returns:
        Script display name (e.g. 'Latin', 'Cyrillic', 'Common'), or None.
    """
    if len(char) != 1:
        return None
    script_getter = getattr(ud, 'script', None)
    if script_getter is not None:
        try:
            code = script_getter(char)
            return script_display.get(code, code) if code else None
        except (ValueError, TypeError):
            pass
    try:
        name = ud.name(char)
    except ValueError:
        return None
    if not name:
        return None
    first = name.split()[0] if name else ''
    return name_prefix_to_script.get(first, 'Common')


def get_html_entity(char: str) -> str:
    """Return the decimal HTML numeric character reference (e.g. '&#107;' for 'k').

    Args:
        char: Single Unicode character.

    Returns:
        String of the form '&#decimal;'.
    """
    if len(char) != 1:
        raise ValueError(f"get_html_entity expects a single character, got length {len(char)}")
    return f'&#{ord(char)};'


def get_utf8_bytes(char: str) -> str:
    """Return the UTF-8 byte representation of the character as hex (e.g. '0x6B' for 'k').

    Multi-byte sequences are space-separated (e.g. '0xF0 0x9F 0x98 0x80' for '😀').

    Args:
        char: Single Unicode character.

    Returns:
        Hex string of the form '0xXX' or '0xXX 0xYY ...'.
    """
    if len(char) != 1:
        raise ValueError(f"get_utf8_bytes expects a single character, got length {len(char)}")
    return ' '.join(f'0x{b:02X}' for b in char.encode('utf-8'))


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
            utf8_bytes=get_utf8_bytes(char),
            html_entity=get_html_entity(char),
            script=get_script(char),
            homoglyph_risk=get_homoglyph_risk(char),
            invisible=get_invisible_warning(char),
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
        normalization_form[form] = is_normalized(form, string)
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


def get_category(char: str) -> Optional[str]:
    """Return a human-readable character general category.

    Args:
        char: Single Unicode character.

    Returns:
        Category label string (e.g. 'UPPERCASE LETTER'), or None if unknown.
    """
    try:
        return category[ud.category(char)]
    except KeyError:
        return None


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
    category: Optional[str]
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
