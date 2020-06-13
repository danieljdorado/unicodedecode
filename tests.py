from django.test import TestCase
import unicodedata as ud


class UnicodeVersionTestCase(TestCase):
    """Check the footer template version."""
    def setUp(self):
        # Footer template unicode version.
        # Update manually in the template if tests fails.
        self.unicode_version = "12.1.0"

    def test_unicode_version(self):
        self.assertEqual(ud.unidata_version, self.unicode_version)
