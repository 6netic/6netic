import requests
from grandpy import wikiapi
import json


def test_wikiapi_page(monkeypatch):
    result = 4097790

    class MockRequestGetPage:
        """That class mocks request.get function """

        def __init__(self, url, params):
            self.url = "http://internet.com"
            self.params = {"format": "json",
                           "action": "any",
                           "list": "any",
                           "gsradius": 4000,
                           "gscoord": "any_coord"
                           }
            self.status_code = 200

        def json(self):
            response = {
                "batchcomplete": "",
                "query": {
                    "geosearch": [{
                        "pageid": 4097790,
                        "ns": 0,
                        "title": "Rue de Leravel",
                        "lat": 23,
                        "lon": 12,
                        "dist": 59.6,
                        "primary": ""
                    },
                    ]}
            }
            return response

    monkeypatch.setattr("requests.get", MockRequestGetPage)
    instance = wikiapi.PlaceInfo()
    page = instance.search_pageid(23, 32)
    assert result == page


def test_wikiapi_description(monkeypatch):
    result = "Imaginons que cette phrase soit relativement longue..."

    class MockRequestGet:
        """ Making a mock for requests.get() """

        def __init__(self, url, params):
            self.url = "http://www.internet.com"
            self.param = {
                "format": "json",
                "action": "query",
                "prop": "extracts",
                "exsectionformat": "plain",
                "exlimit": 1,
                "exchars": 400,
                "explaintext": True,
                "pageids": 416796
            }
            self.status_code = 200

        def json(self):
            response = {
                "batchcomplete": "",
                "query": {
                    "pages":
                        {"5093": {
                            "pageid": 5093,
                            "ns": 0,
                            "title": "Tillandsia araujei tulius",
                            "extract": "Imaginons que cette phrase soit relativement longue..."
                        },
                        }
                }

            }
            return response

    monkeypatch.setattr("requests.get", MockRequestGet)
    instance = wikiapi.PlaceInfo()
    description = instance.search_description(5093)
    assert result == description



