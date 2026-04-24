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

    def test_decode_get_with_s_preserves_boundary_whitespace(self):
        """GET with boundary spaces should preserve exact value."""
        raw_value = '  a  '
        response = self.client.get(reverse('decode'), {'s': raw_value})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial.get('text'), raw_value)
        self.assertEqual(len(response.context['text']), len(raw_value))
        self.assertEqual(response.context['text'][0].char, ' ')
        self.assertEqual(response.context['text'][-1].char, ' ')

    def test_decode_get_with_s_param_empty(self):
        """GET with ?s= or empty s shows home form, not decode results."""
        response = self.client.get(reverse('decode'), {'s': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertNotIn('text', response.context)

    def test_decode_live_post_returns_results_fragment(self):
        """Live POST path should return HTML fragment instead of full page."""
        response = self.client.post(
            reverse('decode'),
            {'text': 'abc'},
            HTTP_X_DECODE_LIVE='1',
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Character Details', content)
        self.assertNotIn('<html', content.lower())
