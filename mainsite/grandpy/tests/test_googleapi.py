from .. googleapi import AddressGps
from django.test import TestCase
from unittest.mock import patch


class MockResponse:
    """ This class mocks Google Api response """

    def __init__(self):
        self.status_code = 200

    def json(self):

        return {
            'results': [
                {'address_components':
                    [
                        {'long_name': 'Cham', 'short_name': 'Cham', 'types': ['locality', 'political']},
                        {'long_name': 'Zug', 'short_name': 'Zug', 'types': ['administrative_area_level_2', 'political']},
                        {'long_name': 'Canton of Zug', 'short_name': 'ZG', 'types': ['administrative_area_level_1', 'political']},
                        {'long_name': 'Switzerland', 'short_name': 'CH', 'types': ['country', 'political']}
                    ],
                'formatted_address': 'Cham, Switzerland',
                'geometry': {
                    'bounds': {
                        'northeast': {'lat': 47.2337707, 'lng': 8.4799078},
                               'southwest': {'lat': 47.16743169999999, 'lng': 8.4148401}
                    },
                    'location': {
                        'lat': 47.181225, 'lng': 8.4592089},
                    'location_type': 'APPROXIMATE',
                    'viewport': {'northeast': {'lat': 47.2337707, 'lng': 8.4799078},
                                 'southwest': {'lat': 47.16743169999999, 'lng': 8.4148401}}
                },
                'place_id': 'ChIJWdZa4NsAkEcRpHqSeMlyzdE', 'types': ['locality', 'political']
                }
            ],
            'status': 'OK'
        }


class GoogleTests(TestCase):
    """ Tests GoogleApi class """

    @patch('requests.get', return_value=MockResponse())
    def test_calculation(self, mock_request_get):
        """ 1- Tests if we can get correct values from Google Geocode API """

        sentence = "Random Address for testing"
        result = AddressGps().calculation(sentence)
        self.assertEqual(result, ["Cham, Switzerland", "Zug", 47.181225,  8.4592089])