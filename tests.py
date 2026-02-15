"""Backend Tests."""


from django.test import TestCase
import unicodedata as ud
import unicodedecode.unicode_util as u


class UnicodeVersionTestCase(TestCase):
    """Check the footer template version."""
    def setUp(self):
        # Footer template unicode version.
        # Update version manually in the template if tests fails.
        self.unicode_version = "12.1.0"

    def test_unicode_version(self):
        """Tests current unicode version to make sure footer gets updated."""
        self.assertEqual(ud.unidata_version, self.unicode_version)


class TestCodePoints(TestCase):
    """Verify codepoint output."""
    def setUp(self):
        self.code_points = {
            'h' : 'U+0068', # LATIN SMALL LETTER H.
            '+' : 'U+002B', # PLUS SIGN.
            'È' : 'U+00C8', # LATIN CAPITAL LETTER E WITH GRAVE.
            'Ć' : 'U+0106', # LATIN CAPITAL LETTER C WITH ACUTE.
            'ķ' : 'U+0137', # LATIN SMALL LETTER K WITH CEDILLA.
            'Ψ' : 'U+03A8', # GREEK CAPITAL LETTER PSI.
            'Ͽ' : 'U+03FF', # GREEK SMALL REVERSED DOTTED LUNATE SIGMA SYMBOL.
            'Ж' : 'U+0416', # CYRILLIC CAPITAL LETTER ZHE.
            'ӹ' : 'U+04F9', # CYRILLIC CAPITAL LETTER YERU WITH DIAERESIS.
            'Ӿ' : 'U+04FE', # CYRILLIC CAPITAL LETTER HA WITH STROKE.
            'Յ' : 'U+0545', # ARMENIAN CAPITAL LETTER YI.
            'ᰇ' : 'U+1C07', # LEPCHA LETTER CHA.
            '၅' : 'U+1045', # MYANMAR DIGIT FIVE.
            'ש' : 'U+05E9', # HEBREW LETTER SHIN.
            'ۻ' : 'U+06FB', # ARABIC LETTER DAD WITH DOT BELOW.
            ' ' : 'U+0020', # SPACE.
            '😀' : 'U+1F600' # GRINNING FACE.
        }


    def test_get_code_point(self):
        """Test get_codepoint output."""
        for char, code_point in self.code_points.items():
            self.assertEqual(u.get_code_point(char), code_point)


class TestNormalization(TestCase):
    """Normalization."""
    def setUp(self):
        """Test examples."""
        self.forms = {
            # U+0061 LATIN SMALL LETTER A.
            'a': {'NFC': True, 'NFKC' : True, 'NFD' : True, 'NFKD' : True},
            # U+00E9 LATIN SMALL LETTER E WITH ACUTE.
            'é' : {'NFC': True, 'NFKC' : True, 'NFD' : False, 'NFKD' : False},
            # U+0065 LATIN SMALL LETTER E.
            # U+0301 COMBINING ACUTE ACCENT.
            'é': {'NFC': False, 'NFKC' : False, 'NFD' : True, 'NFKD' : True},
            # U+FB01 LATIN SMALL LIGATURE FI.
            'ﬁ': {'NFC': True, 'NFKC' : False, 'NFD' : True, 'NFKD' : False},
            # U+1E9B LATIN SMALL LETTER LONG S WITH DOT ABOVE.
            # U+0323 COMBINING DOT BELOW.
            'ẛ̣': {'NFC': True, 'NFKC' : False, 'NFD' : False, 'NFKD' : False},
        }

    def test_normalization_check(self):
        """Normalization."""
        for text, form in self.forms.items():
            text = u.get_normalization_form(text)
            self.assertEqual(text, form)


class TestUnicodeName(TestCase):
    """Test Unicode Names."""
    def setUp(self):
        """Test examples."""

        self.names = {
            ' ' : 'SPACE',
            '😀' : 'GRINNING FACE',
            'ꖣ' : 'VAI SYLLABLE VU',
            '"' : 'QUOTATION MARK',
            '	' : 'CHARACTER TABULATION',
            '˜': 'SMALL TILDE',
        }


    def test_name(self):
        """Get character name test."""
        for char, name in self.names.items():
            self.assertEqual(u.get_name(char), name)


class TestUnicodeDigits(TestCase):
    """Test Unicode Digits."""
    def setUp(self):
        """Test examples."""

        self.digits = {
            '1' : 1, # U+0031 DIGIT ONE.
            '⑩': '', # U+246B CIRCLED NUMBER TWELVE.
            '۵': 5, # U+06F5 EXTENDED ARABIC-INDIC DIGIT FIVE.
            '६': 6, # U+096C DEVANAGARI DIGIT SIX.
            '੧': 1, # U+0A67 GURMUKHI DIGIT ONE.
            '🔟' : '', # U+1F51F KEYCAP TEN.
            '૫' : 5, # U+0AEB GUJARATI DIGIT FIVE.
            'Ⅶ' : '', # U+2166 ROMAN NUMERAL SEVEN.
            '¹' : 1, # U+00B9 SUPERSCRIPT ONE.
            'H' : '', # U+0048 LATIN CAPITAL LETTER H.
        }


    def test_digit(self):
        """Get digit test."""
        for char, digit in self.digits.items():
            self.assertEqual(u.get_digit(char), digit)

