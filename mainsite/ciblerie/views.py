from django.shortcuts import render
from django.http import JsonResponse
from . prepare import Prepare
from .image import Image
from datetime import datetime


def index(request):
    """ Index page of ciblerie application """

    return render(request, "ciblerie/index.html")


def ten_meters(request):
    """ view for ten meters category """

    if request.method == 'POST':
        if not request.FILES:
            return JsonResponse(status=417, data={"mess": "Un fichier image doit être sélectionné."})
        else:
            picture = request.FILES['srcfile']
            in_dir, out_dir = Prepare().create_folders()
            picture_validation = Prepare().check_picture(picture)
            if picture_validation == "bad_extension":
                return JsonResponse(status=415, data={"mess": "Seules les extensions jpg, jpeg ou png sont autorisées."})
            elif picture_validation == "too_big":
                return JsonResponse(status=413, data={"mess": "La taille du fichier ne doit pas excéder 5Mo."})
            # Saves temp file to hard disk in /in directory
            image_on_disk = Prepare().save_to_disk(picture)
            # Opens file encoding to numpy.ndarray
            opencv_image = Prepare().open_picture(image_on_disk)
            # Processing image
            extracted_img = Image().extract_new_picture(opencv_image, 170, 195)
            resp = Image().find_biggest_circle_radius(extracted_img, (3, 3), [40, 70], (3, 3))
            x_center, y_center, radius, excentricity = \
                resp["x_center"], resp["y_center"], resp["radius"], resp['excentricity']
            if excentricity > 0.16:
                return JsonResponse(status=417, data={"mess": "La cible n'a pas pu être reconnue correctement."})
            holes_in_img, points_coord = Image().find_holes(extracted_img)
            Image().get_score(holes_in_img, points_coord, x_center, y_center, radius)
            # Saving final image to 'out/' folder
            Prepare().save_after_treatment(holes_in_img)
            dateNow = datetime.now().strftime('%Y%m%d%H%M%S')
            return JsonResponse(status=200, data={"mess": dateNow})
