from django.db import models


class Nurse(models.Model):
    """ Fields for Nurse Table """

    fullname = models.CharField(max_length=30, blank=False, null=False, unique=True)
    firstname = models.CharField(max_length=20, blank=False, null=False, unique=True)
    mobile = models.CharField(max_length=10, blank=True, null=True, unique=True)
    email = models.CharField(max_length=25, blank=True, null=True, unique=True)
    address = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'nurse'

    def __str__(self):
        return self.fullname


class Tour(models.Model):
    """ Fields for Timeplan Table """

    nurse = models.ForeignKey(Nurse, models.CASCADE)
    jour = models.DateField()
    heure = models.CharField(max_length=5, blank=True, null=True)
    patient = models.CharField(max_length=65, blank=True, null=True)
    addrTel = models.CharField(max_length=255, blank=True, null=True)
    cotation = models.CharField(max_length=255, blank=True, null=True)
    assure = models.CharField(max_length=50, blank=True, null=True)
    honoraire = models.CharField(max_length=50, blank=True, null=True)
    finTraitement = models.CharField(max_length=50, blank=True, null=True)
    commentaires = models.CharField(max_length=255, blank=True, null=True)
    traite = models.BooleanField(default=False, null=False)
    nomTournee = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tour'

    def __str__(self):
        return self.jour


class PlanningModel(models.Model):
    """ Fields for PlanningModel Table """

    dateTour = models.DateField(auto_now=False, null=True, blank=False)
    tour1 = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='nurse_tour1')
    tour2 = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='nurse_tour2')

    class Meta:
        managed = True
        db_table = 'planningmodel'

    def __str__(self):
        return self.dateTour







