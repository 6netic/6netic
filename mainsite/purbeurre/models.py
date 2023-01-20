from django.db import models


class Category(models.Model):
    """ This class builds Category table """

    name = models.CharField(max_length=20, unique=True)

    class Meta:
        managed = True
        db_table = 'category'


class Product(models.Model):
    """ This class builds Product table """

    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    nutrition_grade = models.CharField(max_length=1, blank=True, null=True)
    barcode = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    url_pic = models.CharField(max_length=255, blank=True, null=True)
    store = models.CharField(max_length=255, blank=True, null=True)
    prd_cat = models.ForeignKey(Category, models.DO_NOTHING, db_column='prd_cat')
    fat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    saturated_fat = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    sugar = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    salt = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'


class Favourite(models.Model):
    """ This class builds Favourite table """

    former_barcode = models.CharField(max_length=80)
    favourite_barcode = models.CharField(max_length=80, unique=True)
    email_user = models.EmailField(max_length=150)

    class Meta:
        managed = True
        db_table = 'favourite'


