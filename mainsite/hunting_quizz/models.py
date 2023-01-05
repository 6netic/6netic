from django.db import models


class Hunting(models.Model):
    """ Fields for hunting table """

    question = models.CharField(max_length=255, null=True)
    opt1 = models.CharField(max_length=200, null=True),
    opt2 = models.CharField(max_length=200, null=True),
    opt3 = models.CharField(max_length=200, null=True),
    answer = models.TextField(max_length=400, null=True)

    def __str__(self):
        return self.question