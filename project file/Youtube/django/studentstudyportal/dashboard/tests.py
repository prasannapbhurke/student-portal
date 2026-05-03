from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse


class ExternalSearchFallbackTests(TestCase):
    @override_settings(YOUTUBE_API_KEY='')
    def test_youtube_search_provides_external_link_without_api_key(self):
        response = self.client.get(reverse('youtube'), {'query': 'linear algebra'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Open on YouTube')
        self.assertContains(response, 'https://www.youtube.com/results?search_query=linear+algebra')

    @patch('dashboard.views.requests')
    def test_wiki_search_provides_external_link_when_api_fails(self, mock_requests):
        mock_requests.get.side_effect = Exception('network unavailable')

        response = self.client.get(reverse('wiki'), {'query': 'calculus'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Open Wikipedia')
        self.assertContains(response, 'https://en.wikipedia.org/wiki/Special:Search?search=calculus')
