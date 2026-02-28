"""Tests for decode view (home and ?s= URL parameter)."""

from django.test import Client, TestCase
from django.urls import reverse


class DecodeViewTestCase(TestCase):
    """Views for decode (home) and form submission."""

    def setUp(self):
        self.client = Client()

    def test_decode_get_with_s_param(self):
        """GET with ?s=... shows decode results for that string (e.g. /?s=abcd)."""
        response = self.client.get(reverse('decode'), {'s': 'abcd'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.context)
        self.assertIn('normalization_form', response.context)
        self.assertIsInstance(response.context['text'], list)
        self.assertEqual(len(response.context['text']), 4)
        # Form is prefilled with the query string
        self.assertEqual(response.context['form'].initial.get('text'), 'abcd')

    def test_decode_get_with_s_param_empty(self):
        """GET with ?s= or empty s shows home form, not decode results."""
        response = self.client.get(reverse('decode'), {'s': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertNotIn('text', response.context)
