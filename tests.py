"""Backend tests for unicodedecode app."""

from django.test import TestCase, Client
from django.urls import reverse
import unicodedata as ud
import unicodedecode.unicode_util as u


class UnicodeVersionTestCase(TestCase):
    """Check the footer template version."""
    def setUp(self):
        # Footer template unicode version.
        # Update version manually in the template if tests fail.
        self.unicode_version = "12.1.0"

    def test_unicode_version_exact(self):
        """Current unicode version matches expected for footer."""
        self.assertEqual(ud.unidata_version, self.unicode_version)

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
            '😀': 'U+1F600',  # GRINNING FACE
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


class TestNormalization(TestCase):
    """Normalization form detection."""
    def setUp(self):
        self.forms = {
            'a': {'NFC': True, 'NFKC': True, 'NFD': True, 'NFKD': True},
            'é': {'NFC': True, 'NFKC': True, 'NFD': False, 'NFKD': False},
            'é': {'NFC': False, 'NFKC': False, 'NFD': True, 'NFKD': True},  # e + combining acute
            'ﬁ': {'NFC': True, 'NFKC': False, 'NFD': True, 'NFKD': False},
            'ẛ̣': {'NFC': True, 'NFKC': False, 'NFD': False, 'NFKD': False},
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
        self.assertEqual(set(result.keys()), {'NFC', 'NFKC', 'NFD', 'NFKD'})
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
            '⑩': '',     # U+2469 CIRCLED NUMBER TEN (digit may be 10 or not defined)
            '۵': 5,      # U+06F5 EXTENDED ARABIC-INDIC DIGIT FIVE
            '६': 6,      # U+096C DEVANAGARI DIGIT SIX
            '੧': 1,      # U+0A67 GURMUKHI DIGIT ONE
            '🔟': '',    # U+1F51F KEYCAP TEN
            '૫': 5,      # U+0AEB GUJARATI DIGIT FIVE
            'Ⅶ': '',     # U+2166 ROMAN NUMERAL SEVEN
            '¹': 1,      # U+00B9 SUPERSCRIPT ONE
            'H': '',     # U+0048 LATIN CAPITAL LETTER H
        }

    def test_digit(self):
        """get_digit returns numeric value or empty string."""
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

    def test_returns_string(self):
        """get_direction always returns a string (possibly empty)."""
        self.assertIsInstance(u.get_direction('A'), str)
        self.assertIsInstance(u.get_direction(' '), str)


class TestGetEastAsianWidth(TestCase):
    """East Asian width category."""
    def test_returns_string(self):
        self.assertIsInstance(u.get_east_asian_width('A'), str)
        self.assertIsInstance(u.get_east_asian_width('　'), str)

    def test_known_categories(self):
        """Common characters have a non-empty width label."""
        self.assertTrue(len(u.get_east_asian_width('A')) > 0)
        self.assertTrue(len(u.get_east_asian_width('あ')) > 0)


class TestExamenUnicode(TestCase):
    """examen_unicode builds per-character attribute list."""
    REQUIRED_KEYS = {'char', 'name', 'category', 'digit', 'bidi', 'ord', 'code_point', 'hex'}

    def test_empty_string(self):
        """Empty string returns empty list."""
        self.assertEqual(u.examen_unicode(''), [])

    def test_single_character(self):
        """Single character returns one dict with all required keys."""
        result = u.examen_unicode('A')
        self.assertEqual(len(result), 1)
        self.assertEqual(set(result[0].keys()), self.REQUIRED_KEYS)
        self.assertEqual(result[0]['char'], 'A')
        self.assertEqual(result[0]['ord'], 65)
        self.assertEqual(result[0]['code_point'], 'U+0041')
        self.assertEqual(result[0]['hex'], '0041')

    def test_multiple_characters(self):
        """Multiple characters return one dict per character."""
        result = u.examen_unicode('Hi')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['char'], 'H')
        self.assertEqual(result[1]['char'], 'i')

    def test_unicode_string(self):
        """Non-ASCII and emoji are handled."""
        result = u.examen_unicode('😀')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['char'], '😀')
        self.assertEqual(result[0]['code_point'], 'U+1F600')


class TestAlias(TestCase):
    """Alias lookup from NameAliases.txt."""
    def test_get_aliases_list(self):
        """get_aliases with format=False returns a list."""
        aliases = u.alias.get_aliases('A', format=False)
        self.assertIsInstance(aliases, list)

    def test_get_aliases_formatted(self):
        """get_aliases with format=True returns comma-separated string."""
        result = u.alias.get_aliases('A', format=True)
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

    def test_returns_all_keys(self):
        """Returned dict has all keys needed by codepoint template."""
        desc = u.get_character_page_description('A')
        self.assertEqual(set(desc.keys()), self.REQUIRED_KEYS)

    def test_values_sensible(self):
        """Values are correct types and consistent."""
        desc = u.get_character_page_description('a')
        self.assertEqual(desc['char'], 'a')
        self.assertEqual(desc['name'], 'LATIN SMALL LETTER A')
        self.assertEqual(desc['tagline'], 'U+0061')
        self.assertEqual(desc['integer'], 97)
        self.assertEqual(desc['upper'], 'A')
        self.assertEqual(desc['lower'], 'a')
        self.assertIsInstance(desc['decomposition'], str)
        self.assertIsInstance(desc['aliases'], str)
        self.assertIsInstance(desc['east_asian'], str)


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

