from .. wikiapi import PlaceInfo
from django.test import TestCase
from unittest.mock import patch


class MockResponseInSearchPageId:
    """ This class mocks requests.get function in search_pageid method """

    def __init__(self):
        self.status_code = 200


    def json(self):

        return {
            'batchcomplete': '',
            'query': {'geosearch': [
                {'pageid': 1364337, 'ns': 0, 'title': 'Hôtel de Beauvau', 'lat': 48.8713, 'lon': 2.31643,
                 'dist': 4, 'primary': ''},
                {'pageid': 4408555, 'ns': 0, 'title': 'Faubourg Saint-Honoré', 'lat': 48.871109, 'lon': 2.316313,
                 'dist': 18.9, 'primary': ''},
                {'pageid': 722651, 'ns': 0, 'title': 'Place Beauvau', 'lat': 48.871081, 'lon': 2.316236,
                 'dist': 24.4, 'primary': ''},
                {'pageid': 3660677, 'ns': 0, 'title': 'Rue du Cirque (Paris)', 'lat': 48.871088, 'lon': 2.315422,
                 'dist': 75.4, 'primary': ''},
                {'pageid': 1791353, 'ns': 0, 'title': 'Rue des Saussaies', 'lat': 48.87125, 'lon': 2.3175,
                 'dist': 79.2, 'primary': ''},
                {'pageid': 8642659, 'ns': 0, 'title': 'Service central du renseignement territorial', 'lat': 48.871353,
                 'lon': 2.31756, 'dist': 84.1, 'primary': ''},
                {'pageid': 849892, 'ns': 0, 'title': "Ministère de l'Intérieur (France)", 'lat': 48.871944444444,
                 'lon': 2.3169444444444, 'dist': 84.8, 'primary': ''},
                {'pageid': 24066, 'ns': 0, 'title': 'Police nationale (France)', 'lat': 48.871469, 'lon': 2.317706,
                 'dist': 96.9, 'primary': ''},
                {'pageid': 3652124, 'ns': 0, 'title': 'Rue de Duras', 'lat': 48.870878, 'lon': 2.317868,
                 'dist': 114.5, 'primary': ''},
                {'pageid': 1116653, 'ns': 0, 'title': 'Hôtel de Marigny', 'lat': 48.870555555556,
                 'lon': 2.3152777777778, 'dist': 114.8, 'primary': ''}
            ]}
        }


class MockResponseInSearchDescription:
    """ This class mocks requests.get function in search_description method """

    def __init__(self):
        self.status_code = 200


    def json(self):

        return {
            'batchcomplete': '',
            'query': {
                'pages': {
                    '1364337': {
                        'pageid': 1364337,
                        'ns': 0,
                        'title': 'Hôtel de Beauvau',
                        'extract': "L’hôtel de Beauvau est un hôtel particulier situé place Beauvau, à Paris. Il est le "
                                   "siège du ministère français de l'Intérieur depuis 1861 (le ministre y possède "
                                   "également un appartement de fonction) et se trouve à proximité du palais de l'Élysée."
                                   "\nDans le langage courant, et notamment dans les médias, le ministre de l'Intérieur "
                                   "est souvent désigné par l'expression « locataire de Beauvau ».\nLa protection du "
                                   "complexe ministériel, comprenant l'hôtel..."
                    }
                }
            }
        }


class PlaceInfoTest1(TestCase):
    """ Tests fisrt part of PlaceInfo class """

    @patch('requests.get', return_value=MockResponseInSearchPageId())
    def test_search_pageid(self, mock_request_get):
        """ 1- Tests if we can get page id from Google Api """

        result = PlaceInfo().search_pageid(34.052, 78.002)
        self.assertEqual(result, 1364337)


class PlaceInfoTest2(TestCase):
    """ Tests second part of PlaceInfo class """

    @patch('requests.get', return_value=MockResponseInSearchDescription())
    def test_search_description(self, mock_request_get):
        """ 2- Tests if we can get short description of the page from Google Api """

        result = PlaceInfo().search_description(1364337)
        self.assertEqual(result, "L’hôtel de Beauvau est un hôtel particulier situé place Beauvau, à Paris. Il est le "
                                   "siège du ministère français de l'Intérieur depuis 1861 (le ministre y possède "
                                   "également un appartement de fonction) et se trouve à proximité du palais de l'Élysée."
                                   "\nDans le langage courant, et notamment dans les médias, le ministre de l'Intérieur "
                                   "est souvent désigné par l'expression « locataire de Beauvau ».\nLa protection du "
                                   "complexe ministériel, comprenant l'hôtel..."
                         )
