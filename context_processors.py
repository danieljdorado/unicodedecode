"""Template context processors for the decode app."""

import unicodedata2


def unicode_version(request):
    """Add Unicode data version from unicodedata2 to every template context."""
    return {'unicode_version': unicodedata2.unidata_version}
