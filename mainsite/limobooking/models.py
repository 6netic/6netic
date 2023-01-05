from django.db import models

class Booking(models.Model):
    """ Database for Bookings app """

    destination = models.CharField('Destination', max_length=250)
    departureDate = models.DateField('Date de départ')
    departureTime = models.CharField('Heure de départ', max_length=5)
    sharing = models.CharField('Partage', max_length=3)
    firstname = models.CharField('Prénom', max_length=250)
    lastname = models.CharField('Nom de famille', max_length=250)
    email = models.EmailField('Email', max_length=70)
    price = models.DecimalField('Prix', max_digits=6, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'booking'
        unique_together = ('destination', 'departureDate', 'email')
