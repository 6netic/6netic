from django.contrib import admin
from .models import Hunting, Response


class CustomDBModelAdmin(admin.ModelAdmin):
    """ Custom class to provide admin interface for the model on Hunting database """

    using = 'huntingquizz'

    def save_model(self, request, obj, form, change):
        """ Saves objects to 'huntingquizz' database """

        obj.save(using=self.using)

    def get_queryset(self, request):
        """ Looks for objects on 'huntingquizz' database """

        return super().get_queryset(request).using(self.using)


admin.site.register(Hunting, CustomDBModelAdmin)
admin.site.register(Response, CustomDBModelAdmin)