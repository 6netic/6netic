import os
import dotenv
from django.shortcuts import render
from django.http import JsonResponse
from .control import *

dotenv.load_dotenv(os.path.join('.env'))


def index(request):
    """ Homepage when accessing the application """

    googleApiKey = os.getenv("GOOGLE_API_KEY")
    return render(request, 'grandpy/index.html', locals())


def process(request):
    """ That function is treating the request sent by the user """

    if request.method == 'POST':
        search_sentence = request.POST.get('mySearch')
        cleaned_sentence = make_new_sentence(search_sentence)
        coord = find_place(cleaned_sentence)
        address, street_name, latitude, longitude = coord[0], coord[1], coord[2], coord[3]
        page_id = show_page(latitude, longitude)
        description = show_description(page_id)

        return JsonResponse(status=200, data={
            "address": address,
            "street_name": street_name,
            "latitude": latitude,
            "longitude": longitude,
            "pageid": page_id,
            "description": description
        })

