from django.contrib import admin
from . models import Nurse, Tour, PlanningModel


class LorchideeModelAdmin(admin.ModelAdmin):
    """ Custom class to provide admin interface for the model on Hunting database """

    using = 'lorchidee'

    def save_model(self, request, obj, form, change):
        """ Saves objects to 'lorchidee' database """

        obj.save(using=self.using)

    def get_queryset(self, request):
        """ Looks for objects on 'lorchidee' database """

        return super().get_queryset(request).using(self.using)



admin.site.register(Nurse, LorchideeModelAdmin)
admin.site.register(Tour, LorchideeModelAdmin)
admin.site.register(PlanningModel, LorchideeModelAdmin)
