from django.test import TestCase
from .uni import get_codepoint
import unicodedata as ud



class UnicodeVersionTestCase(TestCase):
    """Check the footer template version."""
    def setUp(self):
        # Footer template unicode version.
        # Update version manually in the template if tests fails.
        self.unicode_version = "12.1.0"

    def test_unicode_version(self):
        self.assertEqual(ud.unidata_version, self.unicode_version)


class TestUni(TestCase):
    """Verify codepoint output"""
    def setUp(self):
        self.codepoints = {
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
            ' ' : 'U+0020' # SPACE.
        }

    def test_get_codepoint(self):
        for char, codepoint in self.codepoints.items():
            self.assertEqual(get_codepoint(char), codepoint)
