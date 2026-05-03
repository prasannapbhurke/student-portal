from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from dashboard.models import DictionaryEntry


class ExternalSearchFallbackTests(TestCase):
    @override_settings(YOUTUBE_API_KEY='')
    def test_youtube_search_redirects_without_api_key(self):
        response = self.client.get(reverse('youtube'), {'query': 'linear algebra'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://www.youtube.com/results?search_query=linear+algebra')

    @patch('dashboard.views.requests')
    def test_wiki_search_redirects_to_search_when_api_fails(self, mock_requests):
        mock_requests.get.side_effect = Exception('network unavailable')

        response = self.client.get(reverse('wiki'), {'query': 'calculus'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['Location'],
            'https://en.wikipedia.org/wiki/Special:Search?search=calculus&go=Go'
        )

    @patch('dashboard.views.requests')
    def test_wiki_search_redirects_to_best_matching_article(self, mock_requests):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'query': {
                'search': [
                    {'title': 'Sachin Tendulkar'}
                ]
            }
        }
        mock_requests.get.return_value = mock_response

        response = self.client.get(reverse('wiki'), {'query': 'sachiin tendulakr'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://en.wikipedia.org/wiki/Sachin_Tendulkar')


class DictionaryLookupTests(TestCase):
    def setUp(self):
        DictionaryEntry.objects.create(
            word='student',
            meaning='A person who is studying.',
            pronunciation='/student/',
            example='The student revised every evening.'
        )

    def test_dictionary_returns_closest_local_match(self):
        response = self.client.get(reverse('dictionary'), {'word': 'studant'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Showing closest local match')
        self.assertContains(response, 'student')

    @patch('dashboard.views.fetch_json')
    def test_dictionary_falls_back_to_online_lookup(self, mock_fetch_json):
        mock_fetch_json.return_value = [
            {
                'word': 'analysis',
                'phonetics': [{'text': '/analysis/'}],
                'meanings': [
                    {
                        'definitions': [
                            {
                                'definition': 'Detailed examination of the elements of something.',
                                'example': 'She wrote a careful analysis of the poem.'
                            }
                        ]
                    }
                ]
            }
        ]

        response = self.client.get(reverse('dictionary'), {'word': 'analysis'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Online dictionary lookup')
        self.assertContains(response, 'Detailed examination of the elements of something.')

    @patch('dashboard.views.fetch_json')
    def test_dictionary_redirects_to_external_dictionary_when_lookup_fails(self, mock_fetch_json):
        mock_fetch_json.side_effect = Exception('lookup failed')

        response = self.client.get(reverse('dictionary'), {'word': 'analysis'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://www.dictionary.com/browse/analysis')


class AuthenticationFlowTests(TestCase):
    def test_logout_post_redirects_home(self):
        user = get_user_model().objects.create_user(username='tester', password='secret123')
        self.client.force_login(user)

        response = self.client.post(reverse('logout'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
