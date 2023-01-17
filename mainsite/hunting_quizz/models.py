from django.db import models


class Hunting(models.Model):
    """ Fields for hunting table """

    question = models.CharField(max_length=255, blank=False)
    choice1 = models.CharField(max_length=200, blank=False)
    choice2 = models.CharField(max_length=200, blank=False)
    choice3 = models.CharField(max_length=200, blank=True)
    imgdir = models.CharField(max_length=250, blank=False)
    answer = models.CharField(max_length=200, blank=False)
    ansdesc = models.TextField(max_length=300, blank=False)
    important = models.BooleanField(default=False)

    def __str__(self):
        return self.question


class Response(models.Model):
    """ Fields for answers """

    quest = models.ForeignKey(Hunting, models.CASCADE)
    usranswer = models.CharField(max_length=200, blank=False)

    def __int__(self):
        return self.quest

