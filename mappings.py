# Data Dictionaries.

bidi = {
    'L': 'LEFT-TO-RIGHT',
    'R': 'RIGHT-TO-LEFT (NON-ARABIC)',
    'AL': 'RIGHT-TO-LEFT (ARABIC)',
    'EN': 'EUROPEAN NUMBER',
    'ES': 'EUROPEAN SEPARATOR',
    'ET': 'EUROPEAN TERMINATOR',
    'AN': 'ARABIC NUMBER',
    'CS': 'COMMON SEPARATOR',
    'NSM': 'NONSPACING MARK',
    'BN': 'BOUNDARY NEUTRAL',
}

category = {
    'Lu': 'UPPERCASE LETTER',
    'Ll': 'LOWERCASE LETTER',
    'Lt': 'TITLECASE LETTER',
    'Lm': 'MODIFIER LETTER',
    'Lo': 'OTHER LETTER',
    'Mn': 'NONSPACING MARK',
    'Mc': 'SPACING MARK',
    'Me': 'ENCLOSING MARK',
    'M': 'MARK',
    'Nd': 'DECIMAL NUMBER',
    'Nl': 'LETTER NUMBER',
    'No': 'OTHER NUMBER',
    'Pc': 'CONNECTOR PUNCTUATION',
    'Pd': 'DASH PUNCTUATION',
    'Ps': 'OPEN PUNCTUATION',
    'Pe': 'CLOSE PUNCTUATION',
    'Pi': 'INITIAL PUNCTUATION',
    'Pf': 'FINAL PUNCTUATION',
    'Po': 'OTHER PUNCTUATION',
    'Sm': 'MATH SYMBOL',
    'Sc': 'CURRENCY SYMBOL',
    'Sk': 'MODIFIER SYMBOL',
    'So': 'OTHER SYMBOL',
    'Zs': 'SPACE SEPARATOR',
    'Zl': 'LINE SEPARATOR',
    'Zp': 'PARAGRAPH SEPARATOR',
    'Cc': 'CONTROL',
    'Cf': 'FORMAT',
    'Cs': 'SURROGATE',
    'Co': 'PRIVATE USE',
    'Cn': 'UNASSIGNED',
}

east_asian_categories = {
    'F': 'East Asian Fullwidth',
    'H': 'East Asian Halfwidth',
    'W': 'East Asian Wide',
    'Na': 'East Asian Narrow',
    'A': 'East Asian Ambiguous',
    'N': 'Non East Asian',
}

# Unicode Script property short code -> display name (for homoglyph / lookalike detection).
script_display = {
    'Common': 'Common',
    'Inherited': 'Inherited',
    'Unknown': 'Unknown',
    'Latn': 'Latin',
    'Cyrl': 'Cyrillic',
    'Arab': 'Arabic',
    'Grek': 'Greek',
    'Hebr': 'Hebrew',
    'Hani': 'Han',
    'Hira': 'Hiragana',
    'Kana': 'Katakana',
    'Hang': 'Hangul',
    'Deva': 'Devanagari',
    'Thai': 'Thai',
    'Beng': 'Bengali',
    'Taml': 'Tamil',
    'Telu': 'Telugu',
    'Gujr': 'Gujarati',
    'Knda': 'Kannada',
    'Mlym': 'Malayalam',
    'Mymr': 'Myanmar',
    'Khmr': 'Khmer',
    'Laoo': 'Lao',
    'Tibt': 'Tibetan',
    'Geor': 'Georgian',
    'Armn': 'Armenian',
    'Thaa': 'Thaana',
    'Syrc': 'Syriac',
    'Copt': 'Coptic',
    'Brai': 'Braille',
    'Phag': 'Phags-Pa',
    'Nkoo': 'Nko',
}

# Character name prefix (first word of Unicode name) -> display name when ud.script is unavailable.
name_prefix_to_script = {
    'LATIN': 'Latin',
    'CYRILLIC': 'Cyrillic',
    'ARABIC': 'Arabic',
    'GREEK': 'Greek',
    'HEBREW': 'Hebrew',
    'HAN': 'Han',
    'CJK': 'Han',
    'HIRAGANA': 'Hiragana',
    'KATAKANA': 'Katakana',
    'HANGUL': 'Hangul',
    'DEVANAGARI': 'Devanagari',
    'THAI': 'Thai',
    'BENGALI': 'Bengali',
    'TAMIL': 'Tamil',
    'TELUGU': 'Telugu',
    'GUJARATI': 'Gujarati',
    'KANNADA': 'Kannada',
    'MALAYALAM': 'Malayalam',
    'MYANMAR': 'Myanmar',
    'KHMER': 'Khmer',
    'LAO': 'Lao',
    'TIBETAN': 'Tibetan',
    'GEORGIAN': 'Georgian',
    'ARMENIAN': 'Armenian',
    'THAANA': 'Thaana',
    'SYRIAC': 'Syriac',
    'COPTIC': 'Coptic',
    'BRAILLE': 'Braille',
    'PHAGS-PA': 'Phags-Pa',
    'NKO': 'Nko',
    'COMBINING': 'Inherited',
}

# Code points commonly used in homoglyph/spoofing attacks (look like Latin letters or digits).
# Cyrillic, Greek, and fullwidth ASCII variants that can deceive in domains, usernames, etc.
# See Unicode confusables (UTR 39) and homograph attack documentation.
HOMOGLYPH_CODEPOINTS = frozenset({
    # Cyrillic small (look like Latin a, e, o, p, c, y, x, etc.)
    0x0430, 0x0435, 0x043E, 0x0440, 0x0441, 0x0443, 0x0445, 0x0438, 0x043D, 0x0432,
    0x043A, 0x043C, 0x043F, 0x0442, 0x0444, 0x0433, 0x0436, 0x0431, 0x0439, 0x0437,
    0x0434, 0x043B, 0x044C, 0x044F, 0x0447, 0x0448, 0x0449, 0x044B, 0x044D, 0x044E,
    0x044A, 0x0454, 0x0456, 0x0457, 0x0491, 0x0455, 0x0475, 0x0458,  # ѕ, ѵ, ј
    # Cyrillic capital (look like Latin A, B, E, K, M, H, O, P, C, T, Y, X, etc.)
    0x0410, 0x0412, 0x0415, 0x041A, 0x041C, 0x041D, 0x041E, 0x041F, 0x0420, 0x0421,
    0x0422, 0x0423, 0x0425, 0x0413, 0x0417, 0x0411, 0x0418, 0x0414, 0x041B, 0x0424,
    0x0427, 0x0428, 0x0429, 0x042B, 0x042D, 0x042E, 0x042F, 0x0404, 0x0406, 0x0407,
    # Greek small (α, β, ε, ο, etc. look like Latin)
    0x03B1, 0x03B2, 0x03B5, 0x03B7, 0x03B9, 0x03BA, 0x03BC, 0x03BD, 0x03BF, 0x03C0,
    0x03C1, 0x03C2, 0x03C3, 0x03C4, 0x03C5, 0x03C6, 0x03C7, 0x03C8, 0x03B4, 0x03B8,
    0x03BB, 0x03BE, 0x03B6,
    # Greek capital (Α, Β, Ε, etc.)
    0x0391, 0x0392, 0x0395, 0x0396, 0x0397, 0x0399, 0x039A, 0x039C, 0x039D, 0x039F,
    0x03A0, 0x03A1, 0x03A4, 0x03A5, 0x03A7, 0x0393, 0x0394, 0x0398, 0x039B, 0x039E,
    0x03A3, 0x03A6, 0x03A8, 0x03A9,
})
# Fullwidth ASCII (U+FF01..U+FF5E): often used in spoofing; checked by range in is_homoglyph_codepoint.


def is_homoglyph_codepoint(cp: int) -> bool:
    """True if code point is in curated homoglyph set (Cyrillic/Greek/fullwidth lookalikes)."""
    if 0xFF01 <= cp <= 0xFF5E:  # Fullwidth ASCII
        return True
    return cp in HOMOGLYPH_CODEPOINTS


# Invisible / zero-width characters: codepoint -> short label for UI.
INVISIBLE_CHARACTERS = {
    0x200B: 'Zero-width space',
    0x200C: 'Zero-width non-joiner',
    0x200D: 'Zero-width joiner',
    0x200E: 'Left-to-right mark',
    0x200F: 'Right-to-left mark',
    0x202A: 'Left-to-right embedding',
    0x202B: 'Right-to-left embedding',
    0x202C: 'Pop directional formatting',
    0x202D: 'Left-to-right override',
    0x202E: 'Right-to-left override',
    0x2060: 'Word joiner',
    0x2061: 'Function application',
    0x2062: 'Invisible times',
    0x2063: 'Invisible separator',
    0x2064: 'Invisible plus',
    0xFEFF: 'Zero-width no-break space (BOM)',
    0x034F: 'Combining grapheme joiner',
    0x180E: 'Mongolian vowel separator',
    0x00AD: 'Soft hyphen',
}