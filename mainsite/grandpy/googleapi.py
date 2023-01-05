import requests
import os
import dotenv

dotenv.load_dotenv(os.path.join('.env'))

class AddressGps:
    """ This class deals with requesting GoogleMap api """

    def __init__(self):
        """ Initializing the object """

        self.google_api_url = "https://maps.googleapis.com/maps/api/geocode/json?parameters"
        self.google_api_key = os.getenv("GOOGLE_API_KEY")


    def calculation(self, sentence):
        """ Returns an address and its coordinates """

        parameters = {"address": sentence,
                      "key": self.google_api_key,
                      "region": "fr",
                      }
        response = requests.get(self.google_api_url, parameters)

        if response.status_code != 200:
            return False
        else:
            content = response.json()
            results = content["results"]
            address = results[0]["formatted_address"]
            street_name = results[0]["address_components"][1]["long_name"]
            latitude = results[0]["geometry"]["location"]["lat"]
            longitude = results[0]["geometry"]["location"]["lng"]
            coord = [address, street_name, latitude, longitude]
            return coord

