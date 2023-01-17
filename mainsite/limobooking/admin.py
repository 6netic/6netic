from django.contrib import admin
from . models import Booking


class BookingModelAdmin(admin.ModelAdmin):
    """ Custom class to provide admin interface for the model on Hunting database """

    using = 'limobooking'

    def save_model(self, request, obj, form, change):
        """ Saves objects to 'lorchidee' database """

        obj.save(using=self.using)

    def get_queryset(self, request):
        """ Looks for objects on 'lorchidee' database """

        return super().get_queryset(request).using(self.using)



admin.site.register(Booking, BookingModelAdmin)
