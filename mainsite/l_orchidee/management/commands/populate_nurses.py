from django.core.management.base import BaseCommand
from ...models import Nurse


class Command(BaseCommand):
    """ Populate nurses database """

    help = "Does something"

    def handle(self, *args, **options):
        """ Liste des infirmières """

        nurse_list = [
            ["Infirmière 1", "Inf-1", "0601010101", "inf1@gmail.com", "Adresse inconnue"],
            ["Infirmière 2", "Inf-2", "0601010102", "inf2@gmail.com", "Adresse inconnue"],
            ["Infirmière 3", "Inf-3", "0601010103", "inf3@gmail.com", "Adresse inconnue"],
            ["Infirmière 4", "Inf-4", "0601010104", "inf4@gmail.com", "Adresse inconnue"]
        ]
        try:
            for line in nurse_list:
                Nurse.objects.using('lorchidee').create(
                    fullname=line[0],
                    firstname=line[1],
                    mobile=line[2],
                    email=line[3],
                    address=line[4]
                )
            print("Les infirmières ont bien été enregistrées.")
        except:
            print("Une erreur s'est produite.")