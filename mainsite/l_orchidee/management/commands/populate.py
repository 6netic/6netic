from django.core.management.base import BaseCommand
from ...models import Nurse


class Command(BaseCommand):
    """ Populate nurses database """

    help = "Does something"

    def handle(self, *args, **options):
        """ Liste des infirmières """

        nurse_list = [
            ["Ramata Samake", "Ramata", "0652226124", "samakeramata@hotmail.fr", "12 Chemin des Pipeaux, 95800 Cergy"],
            ["Amaria Ghernoug", "Amaria","0646523475", "amaria48@hotmail.fr", "Adresse inconnue"],
            ["Béatrice Wabel", "Béatrice", "0603792129", "wablebeatrice@yahoo.fr", "Adresse inconnue"],
            ["Sonia Roubehi", "Sonia","0783451675", "s.roubehi@yahoo.fr", "Adresse inconnue"]
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