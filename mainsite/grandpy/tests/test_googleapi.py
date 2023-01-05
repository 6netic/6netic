import requests
from grandpy import googleapi
import json


def test_googleapi(monkeypatch):
    result = ["12 Rue des Pains Perdus", "Quartier Lumière", 12, 2.3]

    class MockRequestGet:
        """ Making a mock for requests.get() """

        def __init__(self, url, params):
            self.url = "http://www.internet.com"
            self.params = {"address": "Rue des Deux", "key": "dRt0tuyiG1", "region": "es"}
            self.status_code = 200

        def json(self):
            response = {
                'results': [{
                    'formatted_address': result[0],
                    'address_components': [{}, {'long_name': result[1]}],
                    'geometry': {'location': {'lat': result[2], 'lng': result[3]}},
                }]
            }
            return response

    monkeypatch.setattr("requests.get", MockRequestGet)
    instance = googleapi.AddressGps()
    coord = instance.calculation("Je cherche un restaurant à Blois")
    assert result == coord
