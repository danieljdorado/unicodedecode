"""Backend tests for decode app."""

import dataclasses
from django.test import TestCase, Client
from django.urls import reverse
import unicodedata2 as ud
import decode.unicode_util as u


class UnicodeVersionTestCase(TestCase):
    """Check the footer template version comes from unicodedata2."""
    def test_footer_shows_unicode_version(self):
        """Footer displays current unicodedata2 version."""
        response = self.client.get(reverse('decode'))
        self.assertContains(response, ud.unidata_version)

    def test_unicode_version_format(self):
        """Unicode version string has expected x.y.z format."""
        self.assertIsInstance(ud.unidata_version, str)
        self.assertRegex(ud.unidata_version, r'^\d+\.\d+(\.\d+)?$',
                         'unidata_version should be like 12.1.0')


class TestCodePoints(TestCase):
    """Verify codepoint output."""
    def setUp(self):
        self.code_points = {
            'h': 'U+0068',   # LATIN SMALL LETTER H
            '+': 'U+002B',   # PLUS SIGN
            'È': 'U+00C8',   # LATIN CAPITAL LETTER E WITH GRAVE
            'Ć': 'U+0106',   # LATIN CAPITAL LETTER C WITH ACUTE
            'ķ': 'U+0137',   # LATIN SMALL LETTER K WITH CEDILLA
            'Ψ': 'U+03A8',   # GREEK CAPITAL LETTER PSI
            'Ͽ': 'U+03FF',   # GREEK SMALL REVERSED DOTTED LUNATE SIGMA SYMBOL
            'Ж': 'U+0416',   # CYRILLIC CAPITAL LETTER ZHE
            'ӹ': 'U+04F9',   # CYRILLIC CAPITAL LETTER YERU WITH DIAERESIS
            'Ӿ': 'U+04FE',   # CYRILLIC CAPITAL LETTER HA WITH STROKE
            'Յ': 'U+0545',   # ARMENIAN CAPITAL LETTER YI
            'ᰇ': 'U+1C07',   # LEPCHA LETTER CHA
            '၅': 'U+1045',   # MYANMAR DIGIT FIVE
            'ש': 'U+05E9',   # HEBREW LETTER SHIN
            'ۻ': 'U+06FB',   # ARABIC LETTER DAD WITH DOT BELOW
            ' ': 'U+0020',   # SPACE
            '😀': 'U+1F600',   # GRINNING FACE
            '🫪': 'U+1FAEA',    # DISTORTED FACE
            '🫍': 'U+1FACD'   # ORCA
        }

    def test_get_code_point_with_prefix(self):
        """get_code_point(prefix=True) returns U+XXXX form."""
        for char, code_point in self.code_points.items():
            with self.subTest(char=char, code_point=code_point):
                self.assertEqual(u.get_code_point(char), code_point)
                self.assertEqual(u.get_code_point(char, prefix=True), code_point)

    def test_get_code_point_without_prefix(self):
        """get_code_point(prefix=False) returns bare uppercase hex."""
        cases = [
            ('A', '0041'),
            (' ', '0020'),
            ('😀', '1F600'),
            ('\u0000', '0000'),
        ]
        for char, expected_hex in cases:
            with self.subTest(char=repr(char), expected=expected_hex):
                self.assertEqual(u.get_code_point(char, prefix=False), expected_hex)

    def test_get_code_point_supplementary(self):
        """Code points above U+FFFF are formatted with 4–6 hex digits."""
        # U+1F600 GRINNING FACE
        self.assertEqual(u.get_code_point('😀', prefix=False), '1F600')
        self.assertEqual(u.get_code_point('😀', prefix=True), 'U+1F600')

    def test_get_code_point_requires_single_character(self):
        """get_code_point raises ValueError for empty or multi-character input."""
        with self.assertRaises(ValueError) as cm:
            u.get_code_point('')
        self.assertIn('single character', str(cm.exception))
        self.assertIn('length 0', str(cm.exception))
        with self.assertRaises(ValueError) as cm:
            u.get_code_point('ab')
        self.assertIn('single character', str(cm.exception))
        self.assertIn('length 2', str(cm.exception))


class TestIsNormalized(TestCase):
    """Unit tests for is_normalized(form, s)."""

    def test_empty_string_all_forms(self):
        """Empty string is normalized in every form."""
        for form in u.NormalizationForm:
            with self.subTest(form=form):
                self.assertTrue(u.is_normalized(form, ''))

    def test_ascii_all_forms(self):
        """ASCII letters and digits are typically normalized in all forms."""
        for s in ('a', 'Z', '0', '9', 'Hello', ' \t\n'):
            with self.subTest(s=repr(s)):
                for form in u.NormalizationForm:
                    self.assertTrue(u.is_normalized(form, s), f'{form} {repr(s)}')

    def test_nfc_precomposed_is_nfc(self):
        """Precomposed characters (single codepoint) are NFC."""
        # é = U+00E9 (single precomposed char)
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFC, 'é'))
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFC, 'ñ'))
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFC, 'ü'))

    def test_nfc_decomposed_is_not_nfc(self):
        """Decomposed sequence (base + combining) is not NFC."""
        # e + U+0301 COMBINING ACUTE
        decomposed_e_acute = 'e\u0301'
        self.assertFalse(u.is_normalized(u.NormalizationForm.NFC, decomposed_e_acute))
        self.assertEqual(ud.normalize('NFC', decomposed_e_acute), 'é')

    def test_nfd_decomposed_is_nfd(self):
        """Decomposed sequence is NFD."""
        decomposed_e_acute = 'e\u0301'
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFD, decomposed_e_acute))

    def test_nfd_precomposed_is_not_nfd(self):
        """Precomposed character is not NFD (decomposed form has multiple codepoints)."""
        self.assertFalse(u.is_normalized(u.NormalizationForm.NFD, 'é'))
        self.assertEqual(ud.normalize('NFD', 'é'), 'e\u0301')

    def test_nfkc_compatibility_composite(self):
        """Compatibility composite (e.g. ﬁ) is NFC but not NFKC."""
        # U+FB01 LATIN SMALL LIGATURE FI
        fi_ligature = '\uFB01'
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFC, fi_ligature))
        self.assertFalse(u.is_normalized(u.NormalizationForm.NFKC, fi_ligature))
        self.assertEqual(ud.normalize('NFKC', fi_ligature), 'fi')

    def test_nfkc_after_normalize_is_normalized(self):
        """String normalized to NFKC is is_normalized('NFKC', ...) True."""
        fi_ligature = '\uFB01'
        nfkc = ud.normalize('NFKC', fi_ligature)
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFKC, nfkc))

    def test_nfkd_decomposed_compatibility(self):
        """NFKD decomposes compatibility characters."""
        fi_ligature = '\uFB01'
        self.assertFalse(u.is_normalized(u.NormalizationForm.NFKD, fi_ligature))
        nfkd = ud.normalize('NFKD', fi_ligature)
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFKD, nfkd))

    def test_is_normalized_equals_normalize_equality(self):
        """is_normalized(form, s) matches (s == ud.normalize(form, s))."""
        cases = [
            '',
            'a',
            'é',
            'e\u0301',
            '\uFB01',   # ﬁ
            'ẛ\u0323',  # ẛ̣ (dot above + dot below)
            'café',
            'cafe\u0301',
            '😀',
            '2\u2075',   # 2⁵
        ]
        for s in cases:
            for form in u.NormalizationForm:
                with self.subTest(form=form, s=repr(s)):
                    expected = (s == ud.normalize(form.value, s))
                    self.assertIs(u.is_normalized(form, s), expected)

    def test_each_form_independently(self):
        """Each form gives correct True/False for known strings."""
        # (string, form, expected)
        cases = [
            ('é', u.NormalizationForm.NFC, True),
            ('é', u.NormalizationForm.NFD, False),
            ('e\u0301', u.NormalizationForm.NFC, False),
            ('e\u0301', u.NormalizationForm.NFD, True),
            ('\uFB01', u.NormalizationForm.NFC, True),
            ('\uFB01', u.NormalizationForm.NFKC, False),
            ('fi', u.NormalizationForm.NFKC, True),
            ('ẛ\u0323', u.NormalizationForm.NFC, True),
            ('ẛ\u0323', u.NormalizationForm.NFD, False),
            ('ẛ\u0323', u.NormalizationForm.NFKD, False),
        ]
        for s, form, expected in cases:
            with self.subTest(form=form, s=repr(s), expected=expected):
                self.assertIs(u.is_normalized(form, s), expected)

    def test_return_type_bool(self):
        """is_normalized returns bool."""
        self.assertIsInstance(u.is_normalized(u.NormalizationForm.NFC, ''), bool)
        self.assertIsInstance(u.is_normalized(u.NormalizationForm.NFC, 'x'), bool)
        self.assertIsInstance(u.is_normalized(u.NormalizationForm.NFD, 'é'), bool)

    def test_multiple_combining_marks(self):
        """Multiple combining marks: NFD string is normalized in NFD only when canonical."""
        # a + acute + diaeresis (canonical order)
        a_acute_diaeresis = 'a\u0301\u0308'
        nfd = ud.normalize('NFD', a_acute_diaeresis)
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFD, nfd))
        # If we had wrong order, might not be NFD
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFD, ud.normalize('NFD', 'ä\u0301')))

    def test_emoji_supplementary_plane(self):
        """Supplementary plane (e.g. emoji) can be NFC/NFD."""
        emoji = '😀'
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFC, emoji))
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFD, emoji))
        nfd_emoji = ud.normalize('NFD', emoji)
        self.assertTrue(u.is_normalized(u.NormalizationForm.NFD, nfd_emoji))


class TestNormalization(TestCase):
    """Normalization form detection."""
    def setUp(self):
        NF = u.NormalizationForm
        self.forms = {
            'a': {NF.NFC: True, NF.NFKC: True, NF.NFD: True, NF.NFKD: True},
            'é': {NF.NFC: True, NF.NFKC: True, NF.NFD: False, NF.NFKD: False},
            'é': {NF.NFC: False, NF.NFKC: False, NF.NFD: True, NF.NFKD: True},  # e + combining acute
            'ﬁ': {NF.NFC: True, NF.NFKC: False, NF.NFD: True, NF.NFKD: False},
            'ẛ̣': {NF.NFC: True, NF.NFKC: False, NF.NFD: False, NF.NFKD: False},
        }

    def test_normalization_check(self):
        """get_normalization_form returns correct dict per form."""
        for text, expected in self.forms.items():
            with self.subTest(text=repr(text)):
                result = u.get_normalization_form(text)
                self.assertEqual(result, expected)

    def test_normalization_returns_all_forms(self):
        """get_normalization_form returns exactly NFC, NFKC, NFD, NFKD."""
        result = u.get_normalization_form('a')
        self.assertEqual(set(result.keys()), set(u.NormalizationForm))
        for v in result.values():
            self.assertIs(v, True)


class TestUnicodeName(TestCase):
    """Unicode character names (and alias fallback)."""
    def setUp(self):
        self.names = {
            ' ': 'SPACE',
            '😀': 'GRINNING FACE',
            'ꖣ': 'VAI SYLLABLE VU',
            '"': 'QUOTATION MARK',
            '\t': 'CHARACTER TABULATION',
            '˜': 'SMALL TILDE',
        }

    def test_get_name(self):
        """get_name returns official name or alias."""
        for char, name in self.names.items():
            with self.subTest(char=repr(char), name=name):
                self.assertEqual(u.get_name(char), name)

    def test_get_name_control_character(self):
        """Control characters without official name use alias when available."""
        # NUL has alias "NULL"
        name = u.get_name('\x00')
        self.assertIsInstance(name, str)
        self.assertTrue(len(name) > 0)


class TestUnicodeDigits(TestCase):
    """Digit value for numeric characters."""
    def setUp(self):
        self.digits = {
            '1': 1,      # U+0031 DIGIT ONE
            '⑩': None,  # U+2469 CIRCLED NUMBER TEN (digit may be 10 or not defined)
            '۵': 5,      # U+06F5 EXTENDED ARABIC-INDIC DIGIT FIVE
            '६': 6,      # U+096C DEVANAGARI DIGIT SIX
            '੧': 1,      # U+0A67 GURMUKHI DIGIT ONE
            '🔟': None,  # U+1F51F KEYCAP TEN
            '૫': 5,      # U+0AEB GUJARATI DIGIT FIVE
            'Ⅶ': None,  # U+2166 ROMAN NUMERAL SEVEN
            '¹': 1,      # U+00B9 SUPERSCRIPT ONE
            'H': None,   # U+0048 LATIN CAPITAL LETTER H
        }

    def test_digit(self):
        """get_digit returns numeric value or None for non-digit."""
        for char, expected in self.digits.items():
            with self.subTest(char=repr(char), expected=expected):
                self.assertEqual(u.get_digit(char), expected)

    def test_digit_decimal_zero_nine(self):
        """ASCII digits 0–9 return 0–9."""
        for i in range(10):
            with self.subTest(digit=i):
                self.assertEqual(u.get_digit(str(i)), i)


class TestGetCategory(TestCase):
    """Character general category mapping."""
    def test_letter_categories(self):
        """Letters map to expected category labels."""
        self.assertEqual(u.get_category('A'), 'UPPERCASE LETTER')
        self.assertEqual(u.get_category('a'), 'LOWERCASE LETTER')
        self.assertEqual(u.get_category('Ψ'), 'UPPERCASE LETTER')

    def test_number_and_punctuation(self):
        """Numbers and punctuation have category strings."""
        self.assertEqual(u.get_category('1'), 'DECIMAL NUMBER')
        self.assertEqual(u.get_category(' '), 'SPACE SEPARATOR')
        self.assertEqual(u.get_category('.'), 'OTHER PUNCTUATION')

    def test_symbol(self):
        """Symbols and marks."""
        self.assertEqual(u.get_category('€'), 'CURRENCY SYMBOL')
        self.assertEqual(u.get_category('😀'), 'OTHER SYMBOL')


class TestGetDirection(TestCase):
    """Bidirectional class labels."""
    def test_ltr(self):
        self.assertEqual(u.get_direction('A'), 'LEFT-TO-RIGHT')
        self.assertEqual(u.get_direction('1'), 'EUROPEAN NUMBER')

    def test_rtl(self):
        self.assertEqual(u.get_direction('א'), 'RIGHT-TO-LEFT (NON-ARABIC)')

    def test_returns_string_or_none(self):
        """get_direction returns str or None."""
        self.assertIsInstance(u.get_direction('A'), str)
        result = u.get_direction(' ')
        self.assertTrue(result is None or isinstance(result, str))


class TestGetEastAsianWidth(TestCase):
    """East Asian width category."""
    def test_returns_string_or_none(self):
        """get_east_asian_width returns str or None."""
        result = u.get_east_asian_width('A')
        self.assertTrue(result is None or isinstance(result, str))
        result = u.get_east_asian_width('　')
        self.assertTrue(result is None or isinstance(result, str))

    def test_known_categories(self):
        """Common characters have a non-empty width label."""
        result_a = u.get_east_asian_width('A')
        self.assertIsNotNone(result_a)
        self.assertGreater(len(result_a), 0)
        result_ja = u.get_east_asian_width('あ')
        self.assertIsNotNone(result_ja)
        self.assertGreater(len(result_ja), 0)


class TestExamenUnicode(TestCase):
    """examen_unicode builds per-character CharacterInfo list."""
    def test_empty_string(self):
        """Empty string returns empty list."""
        self.assertEqual(u.examen_unicode(''), [])

    def test_single_character(self):
        """Single character returns one CharacterInfo with all attributes."""
        result = u.examen_unicode('A')
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], u.CharacterInfo)
        self.assertEqual(result[0].char, 'A')
        self.assertEqual(result[0].ordinal, 65)
        self.assertEqual(result[0].code_point, 'U+0041')
        self.assertEqual(result[0].hex_code, '0041')

    def test_multiple_characters(self):
        """Multiple characters return one CharacterInfo per character."""
        result = u.examen_unicode('Hi')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].char, 'H')
        self.assertEqual(result[1].char, 'i')

    def test_unicode_string(self):
        """Non-ASCII and emoji are handled."""
        result = u.examen_unicode('😀')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].char, '😀')
        self.assertEqual(result[0].code_point, 'U+1F600')


class TestAlias(TestCase):
    """Alias lookup from NameAliases.txt."""
    def test_get_aliases_returns_list(self):
        """get_aliases returns a list of alias strings."""
        aliases = u.alias.get_aliases('A')
        self.assertIsInstance(aliases, list)

    def test_get_aliases_can_be_joined(self):
        """Callers can format aliases manually, e.g. ', '.join(get_aliases(char))."""
        result = ', '.join(u.alias.get_aliases('A'))
        self.assertIsInstance(result, str)

    def test_get_alias_returns_string(self):
        """get_alias returns first alias or 'UNKNOWN'."""
        result = u.alias.get_alias('A')
        self.assertIsInstance(result, str)
        self.assertIn(u.alias.get_alias('x'), (u.get_name('x'), 'UNKNOWN'))


class TestGetCharacterPageDescription(TestCase):
    """get_character_page_description for codepoint detail page."""
    REQUIRED_KEYS = {
        'title', 'tagline', 'char', 'name', 'category', 'digit',
        'direction', 'integer', 'upper', 'lower', 'decomposition',
        'aliases', 'east_asian',
    }

    def test_returns_codepoint_description(self):
        """Returned value is CodepointDescription with all fields needed by template."""
        desc = u.get_character_page_description('A')
        self.assertIsInstance(desc, u.CodepointDescription)
        field_names = {f.name for f in dataclasses.fields(desc)}
        self.assertEqual(field_names, self.REQUIRED_KEYS)

    def test_values_sensible(self):
        """Values are correct types and consistent."""
        desc = u.get_character_page_description('a')
        self.assertEqual(desc.char, 'a')
        self.assertEqual(desc.name, 'LATIN SMALL LETTER A')
        self.assertEqual(desc.tagline, 'U+0061')
        self.assertEqual(desc.integer, 97)
        self.assertEqual(desc.upper, 'A')
        self.assertEqual(desc.lower, 'a')
        self.assertIsInstance(desc.decomposition, str)
        self.assertIsInstance(desc.aliases, str)
        self.assertTrue(desc.east_asian is None or isinstance(desc.east_asian, str))


class DecodeViewTestCase(TestCase):
    """Views for decode (home) and form submission."""
    def setUp(self):
        self.client = Client()

    def test_decode_get(self):
        """GET / returns 200 and a form."""
        response = self.client.get(reverse('decode'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_decode_post_valid(self):
        """POST with valid text returns decode result."""
        response = self.client.post(reverse('decode'), {'text': 'Hello'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.context)
        self.assertIn('normalization_form', response.context)
        self.assertIsInstance(response.context['text'], list)
        self.assertEqual(len(response.context['text']), 5)

    def test_decode_post_empty(self):
        """POST with empty text is invalid (required field); form is re-rendered without decode result."""
        response = self.client.post(reverse('decode'), {'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertNotIn('text', response.context)


class CodepointViewTestCase(TestCase):
    """Codepoint detail view by hex code point slug."""
    def setUp(self):
        self.client = Client()

    def test_codepoint_valid_slug(self):
        """Valid hex slug returns 200 and codepoint info."""
        # U+0041 = 'A'
        response = self.client.get(reverse('codepoint', kwargs={'slug': '41'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['char'], 'A')
        self.assertEqual(response.context['tagline'], 'U+0041')

    def test_codepoint_emoji_slug(self):
        """Supplementary codepoint slug (e.g. emoji) works."""
        response = self.client.get(reverse('codepoint', kwargs={'slug': '1F600'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['char'], '😀')


class StaticPagesTestCase(TestCase):
    """About, terms, privacy, tofu return 200."""
    def setUp(self):
        self.client = Client()

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_terms(self):
        response = self.client.get(reverse('terms'))
        self.assertEqual(response.status_code, 200)

    def test_privacy(self):
        response = self.client.get(reverse('privacy'))
        self.assertEqual(response.status_code, 200)

    def test_tofu(self):
        response = self.client.get(reverse('tofu'))
        self.assertEqual(response.status_code, 200)

