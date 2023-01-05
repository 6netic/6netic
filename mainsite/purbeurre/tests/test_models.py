# Type ./manage.py test purbeurre.tests.test_views -v 2
from django.test import TestCase
from ..models import Category, Product, Favourite, PbUser


class PurbeurreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Category.objects.create(name='Viandes')
        related_cat = Category.objects.create(name='Viandes')
        Product.objects.create(
            name="Produit1",
            description="Desc1",
            nutrition_grade="a",
            barcode="000123",
            url="http://web.fr",
            url_pic="http://site.com/mypic1.jpg",
            store="magasin",
            fat=4,
            saturated_fat=0,
            sugar=2,
            salt=0.0256,
            prd_cat=related_cat
        )
        Favourite.objects.create(
            former_barcode="00123",
            favourite_barcode="00940",
            email_user="paul.jones@internet.com"
        )


    def test_category_name_label(self):
        """ - Testing if Category table field is 'name' """

        cat = Category.objects.get(id=1)
        label_name = cat._meta.get_field('name').verbose_name
        self.assertEqual(label_name, 'name')


    def test_category_name_field_max_length(self):
        """ - Testing length of field name in Category table """
        cat = Category.objects.get(id=1)
        max_length = cat._meta.get_field('name').max_length
        self.assertEqual(max_length, 20)


    def test_product_labels(self):
        """ - Testing if Product table fields have correct label names """

        prd = Product.objects.get(id=1)
        # label name
        label_name = prd._meta.get_field('name').verbose_name
        self.assertEqual(label_name, 'name')
        # label description
        label_name = prd._meta.get_field('description').verbose_name
        self.assertEqual(label_name, 'description')
        # label nutrition_grade
        label_name = prd._meta.get_field('nutrition_grade').name
        self.assertEqual(label_name, 'nutrition_grade')
        # label barcode
        label_name = prd._meta.get_field('barcode').verbose_name
        self.assertEqual(label_name, 'barcode')
        # label url
        label_name = prd._meta.get_field('url').verbose_name
        self.assertEqual(label_name, 'url')
        # label url_pic
        label_name = prd._meta.get_field('url_pic').name
        self.assertEqual(label_name, 'url_pic')
        # label store
        label_name = prd._meta.get_field('store').verbose_name
        self.assertEqual(label_name, 'store')
        # label prd_cat
        label_name = prd._meta.get_field('prd_cat').name
        self.assertEqual(label_name, 'prd_cat')
        # label fat
        label_name = prd._meta.get_field('fat').verbose_name
        self.assertEqual(label_name, 'fat')
        # label saturated_fat
        label_name = prd._meta.get_field('saturated_fat').name
        self.assertEqual(label_name, 'saturated_fat')
        # label sugar
        label_name = prd._meta.get_field('sugar').verbose_name
        self.assertEqual(label_name, 'sugar')
        # label salt
        label_name = prd._meta.get_field('salt').verbose_name
        self.assertEqual(label_name, 'salt')

    def test_product_fields(self):
        """ - Testing field attributes in Product table """

        prd = Product.objects.get(id=1)

        # test the type of name field
        prd_type = prd._meta.get_field('name').get_internal_type()
        self.assertEqual(prd_type, 'CharField')
        # label name
        max_length = prd._meta.get_field('name').max_length
        self.assertEqual(max_length, 255)
        # test blank field in label name
        prd_blank = prd._meta.get_field('name').blank
        self.assertTrue(prd_blank)
        # test null field in label name
        prd_null = prd._meta.get_field('name').null
        self.assertTrue(prd_null)

        # test the type of description field
        prd_type = prd._meta.get_field('description').get_internal_type()
        self.assertEqual(prd_type, 'CharField')
        # label description
        max_length = prd._meta.get_field('description').max_length
        self.assertEqual(max_length, 255)
        # test blank field in label description
        prd_blank = prd._meta.get_field('description').blank
        self.assertTrue(prd_blank)
        # test null field in label description
        prd_null = prd._meta.get_field('description').null
        self.assertTrue(prd_null)

        # test the type of nutrition_grade field
        prd_type = prd._meta.get_field('nutrition_grade').get_internal_type()
        self.assertEqual(prd_type, 'CharField')
        # label nutrition_grade
        max_length = prd._meta.get_field('nutrition_grade').max_length
        self.assertEqual(max_length, 1)
        # test blank field in label nutrition_grade
        prd_blank = prd._meta.get_field('nutrition_grade').blank
        self.assertTrue(prd_blank)
        # test null field in label nutrition_grade
        prd_null = prd._meta.get_field('nutrition_grade').null
        self.assertTrue(prd_null)

        # test the type of barcode field
        prd_type = prd._meta.get_field('barcode').get_internal_type()
        self.assertEqual(prd_type, 'CharField')
        # label barcode
        max_length = prd._meta.get_field('barcode').max_length
        self.assertEqual(max_length, 255)
        # test blank field in label barcode
        prd_blank = prd._meta.get_field('barcode').blank
        self.assertFalse(prd_blank)
        # test null field in label barcode
        prd_null = prd._meta.get_field('barcode').null
        self.assertFalse(prd_null)

        # test the type of url field
        prd_type = prd._meta.get_field('url').get_internal_type()
        self.assertEqual(prd_type, 'CharField')
        # label url
        max_length = prd._meta.get_field('url').max_length
        self.assertEqual(max_length, 255)
        # test blank field in label url
        prd_blank = prd._meta.get_field('url').blank
        self.assertTrue(prd_blank)
        # test null field in label url
        prd_null = prd._meta.get_field('url').null
        self.assertTrue(prd_null)

        # test the type of url_pic field
        prd_type = prd._meta.get_field('url_pic').get_internal_type()
        self.assertEqual(prd_type, 'CharField')
        # label url_pic
        max_length = prd._meta.get_field('url_pic').max_length
        self.assertEqual(max_length, 255)
        # test blank field in label url_pic
        prd_blank = prd._meta.get_field('url_pic').blank
        self.assertTrue(prd_blank)
        # test null field in label url_pic
        prd_null = prd._meta.get_field('url_pic').null
        self.assertTrue(prd_null)

        # test the type of store field
        prd_type = prd._meta.get_field('store').get_internal_type()
        self.assertEqual(prd_type, 'CharField')
        # label store
        max_length = prd._meta.get_field('store').max_length
        self.assertEqual(max_length, 255)
        # test blank field in label store
        prd_blank = prd._meta.get_field('store').blank
        self.assertTrue(prd_blank)
        # test null field in label store
        prd_null = prd._meta.get_field('store').null
        self.assertTrue(prd_null)

        # test the type of fat field
        prd_type = prd._meta.get_field('fat').get_internal_type()
        self.assertEqual(prd_type, 'DecimalField')
        # label fat max digits
        max_digits = prd._meta.get_field('fat').max_digits
        self.assertEqual(max_digits, 5)
        # label fat decimal places
        dec_places = prd._meta.get_field('fat').decimal_places
        self.assertEqual(dec_places, 2)
        # test blank field in label fat
        prd_blank = prd._meta.get_field('fat').blank
        self.assertTrue(prd_blank)
        # test null field in label fat
        prd_null = prd._meta.get_field('fat').null
        self.assertTrue(prd_null)

        # test the type of saturated_fat field
        prd_type = prd._meta.get_field('saturated_fat').get_internal_type()
        self.assertEqual(prd_type, 'DecimalField')
        # label saturated_fat max digits
        max_digits = prd._meta.get_field('saturated_fat').max_digits
        self.assertEqual(max_digits, 5)
        # label saturated_fat decimal places
        dec_places = prd._meta.get_field('saturated_fat').decimal_places
        self.assertEqual(dec_places, 2)
        # test blank field in label saturated_fat
        prd_blank = prd._meta.get_field('saturated_fat').blank
        self.assertTrue(prd_blank)
        # test null field in label saturated_fat
        prd_null = prd._meta.get_field('saturated_fat').null
        self.assertTrue(prd_null)

        # test the type of sugar field
        prd_type = prd._meta.get_field('sugar').get_internal_type()
        self.assertEqual(prd_type, 'DecimalField')
        # label sugar max digits
        max_digits = prd._meta.get_field('sugar').max_digits
        self.assertEqual(max_digits, 5)
        # label sugar decimal places
        dec_places = prd._meta.get_field('sugar').decimal_places
        self.assertEqual(dec_places, 2)
        # test blank field in label sugar
        prd_blank = prd._meta.get_field('sugar').blank
        self.assertTrue(prd_blank)
        # test null field in label sugar
        prd_null = prd._meta.get_field('sugar').null
        self.assertTrue(prd_null)

        # test the type of salt
        prd_type = prd._meta.get_field('salt').get_internal_type()
        self.assertEqual(prd_type, 'DecimalField')
        # label salt max digits
        max_digits = prd._meta.get_field('salt').max_digits
        self.assertEqual(max_digits, 5)
        # label salt decimal places
        dec_places = prd._meta.get_field('salt').decimal_places
        self.assertEqual(dec_places, 2)
        # test blank field in label salt
        prd_blank = prd._meta.get_field('salt').blank
        self.assertTrue(prd_blank)
        # test null field in label salt
        prd_null = prd._meta.get_field('salt').null
        self.assertTrue(prd_null)

        # test the type of prd_cat
        prd_type = prd._meta.get_field('prd_cat').get_internal_type()
        self.assertEqual(prd_type, 'ForeignKey')
        # label db_column
        fk = prd._meta.get_field('prd_cat').db_column
        self.assertEqual(fk, 'prd_cat')
        # test blank field in label prd_cat
        prd_blank = prd._meta.get_field('prd_cat').blank
        self.assertFalse(prd_blank)
        # test null field in label prd_cat
        prd_null = prd._meta.get_field('prd_cat').null
        self.assertFalse(prd_null)

        # Favourite table ----------------------------------------------------

    def test_favourite_labels(self):
        """ - Testing if fields of Favourite table have correct label names """

        fav = Favourite.objects.get(id=1)
        # label former_barcode
        label_name = fav._meta.get_field('former_barcode').name
        self.assertEqual(label_name, 'former_barcode')
        # label favourite_barcode
        label_name = fav._meta.get_field('favourite_barcode').name
        self.assertEqual(label_name, 'favourite_barcode')
        # label email_user
        label_name = fav._meta.get_field('email_user').name
        self.assertEqual(label_name, 'email_user')

    def test_favourite_fields(self):
        """ - Testing field attributes in Favourite table """

        fav = Favourite.objects.get(id=1)

        # test the type of former_barcode field
        fav_type = fav._meta.get_field('former_barcode').get_internal_type()
        self.assertEqual(fav_type, 'CharField')
        # label former_barcode
        max_length = fav._meta.get_field('former_barcode').max_length
        self.assertEqual(max_length, 80)
        # test blank field in label former_barcode
        fav_blank = fav._meta.get_field('former_barcode').blank
        self.assertFalse(fav_blank)
        # test null field in label former_barcode
        fav_null = fav._meta.get_field('former_barcode').null
        self.assertFalse(fav_null)

        # test the type of favourite_barcode field
        fav_type = fav._meta.get_field('favourite_barcode').get_internal_type()
        self.assertEqual(fav_type, 'CharField')
        # label favourite_barcode
        max_length = fav._meta.get_field('favourite_barcode').max_length
        self.assertEqual(max_length, 80)
        # test blank field in label favourite_barcode
        fav_blank = fav._meta.get_field('favourite_barcode').blank
        self.assertFalse(fav_blank)
        # test null field in label favourite_barcode
        fav_null = fav._meta.get_field('favourite_barcode').null
        self.assertFalse(fav_null)

        # test the type of email_user field
        fav_type = fav._meta.get_field('email_user').get_internal_type()
        self.assertEqual(fav_type, 'CharField')
        # label email_user
        max_length = fav._meta.get_field('email_user').max_length
        self.assertEqual(max_length, 150)
        # test blank field in label email_user
        fav_blank = fav._meta.get_field('email_user').blank
        self.assertFalse(fav_blank)
        # test null field in label email_user
        fav_null = fav._meta.get_field('email_user').null
        self.assertFalse(fav_null)

