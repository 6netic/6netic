# ./manage.py test purbeurre.tests.test_models -v 2
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


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


# class PbUserManager(BaseUserManager):
#     """ Custom user model manager where email is the unique identifiers
#         for authentication instead of usernames. """
#
#     def create_user(self, email, password, **extra_fields):
#         """ Create and save a User with the given email and password. """
#
#         if not email:
#             raise ValueError("Vous devez rentrer une adresse email.")
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, related_name='pb_user', **extra_fields)  # rajouter username
#         user.set_password(password)
#         user.save(using='purbeurre')  # could also be user.save(using=self._db)
#         return user
#
#
# class PbUser(AbstractUser):
#     """ This class redifines User model """
#
#     username = models.CharField(
#         verbose_name='Utilisateur',
#         max_length=30,
#         # related_name='u_username'
#     )
#     email = models.EmailField(
#         verbose_name='Adresse Email',
#         max_length=255,
#         unique=True,
#         # related_name='u_email'
#     )
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     objects = PbUserManager()
#
#     def __str__(self):
#         return self.email






