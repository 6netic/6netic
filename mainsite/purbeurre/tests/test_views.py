# To make it work, you must add in psql command : ALTER USER myuser CREATEDB;
# Otherwise, Django won't be able to create the test databases
# Type ./manage.py test purbeurre.tests.test_views -v 2

from django.test import TestCase
from django.urls import reverse
from django.urls import resolve
from ..views import legal, index, connect, disconnect, account, search, detail
from ..views import saveprd, register, showfavourites, modifypassword
from ..models import Product, Favourite, Category, PbUser


class PurbeurreViewPageTestCase(TestCase):
    """ - Testing all views from Purbeurre Application """

    # Giving rights to user for all databases
    databases = '__all__'


    def setUp(self):
        """ Initiates elements """

        # Create and Populate Category table
        fake_category_list = ["cat1", "cat2", "cat3"]
        for cat in fake_category_list:
            Category.objects.using('purbeurre').create(name=cat)
        # Create and populate Product table
        related_cat = Category.objects.using('purbeurre').get(name="cat1")
        fake_product_list = [
            ['Produit1', 'Desc1', 'a', '000123', 'https://web.fr', 'https://stat/1.jpg', 'Magasin', 1, 4, 0, 0, 0.0275],
            ['Produit2', 'Desc2', 'b', '000124', 'https://web.fr', 'https://stat/2.jpg', 'Magasin', 1, 0, 0, 0, 0.02]
        ]
        lines = len(fake_product_list)
        for i in range(lines):
            Product.objects.using('purbeurre').create(
                name=fake_product_list[i][0],
                description=fake_product_list[i][1],
                nutrition_grade=fake_product_list[i][2],
                barcode=fake_product_list[i][3],
                url=fake_product_list[i][4],
                url_pic=fake_product_list[i][5],
                store=fake_product_list[i][6],
                fat=fake_product_list[i][8],
                saturated_fat=fake_product_list[i][9],
                sugar=fake_product_list[i][10],
                salt=fake_product_list[i][11],
                prd_cat=related_cat
            )
        # Create a user
        PbUser.objects.create_user(
            username="John",
            email="fake_email@adibou.com",
            password="myPassword"
        )
        # Creating a favourite product
        Favourite.objects.using('purbeurre').create(
            former_barcode='000123',
            favourite_barcode='000124',
            email_user="fake_email@adibou.com"
        )


    def test_if_legal_url_resolves_to_legal_view(self):
        """ - Testing if 'Legal' url points to 'Legal' view """

        url = resolve('/purbeurre/legal')
        self.assertEqual(url.func, legal)


    def test_if_legal_page_exists(self):
        """ - Tests if 'Legal' view has corresponding template"""

        # Getting legal url
        url = reverse('purbeurre:legal')
        # Getting HttpResponse
        response = self.client.get(url)
        # Checking if 'Legal' view has an existing template
        self.assertEqual(response.status_code, 200)
        # Checking if template used is legal.html
        self.assertTemplateUsed(response, 'purbeurre/legal.html')


    def test_if_index_url_resolves_to_index_view(self):
        """ - Testing if 'Index' url points to 'Index' view """

        url = resolve('/purbeurre/index')
        self.assertEqual(url.func, index)


    def test_if_index_page_exists_and_contains_correct_elements(self):
        """ - Tests if 'Index' view has a template and returns correct elements """

        # Getting index url
        url = reverse('purbeurre:index')
        # Getting HttpResponse
        response = self.client.get(url)
        # Checking if 'Index' view has an existing template
        self.assertEqual(response.status_code, 200)
        # Checking if template used is index.html
        self.assertTemplateUsed(response, 'purbeurre/index.html')
        # Getting content of index page
        html = response.content.decode('utf8')
        # Checking if Bootstrap CSS is present
        self.assertIn('<link href="/static/purbeurre/css/styles.css" rel="stylesheet" />', html)
        # Checking if logo image is present
        self.assertIn('<img id="logo" src="/static/purbeurre/assets/img/logo.png" alt="Pur Beurre Logo">', html)
        # Checking if logo image and website name redirect to index page
        self.assertIn('<a class="navbar-brand" href="/purbeurre/index">', html)
        self.assertIn('<img id="logo" src="/static/purbeurre/assets/img/logo.png" alt="Pur Beurre Logo">', html)
        # Checking if search form is present and redirects to search view
        self.assertIn('<form action="/purbeurre/search" method="get" accept-charset="utf-8">', html)
        self.assertIn('<input type="text" class="form-control" placeholder="Chercher" name="search_word">', html)
        self.assertIn('</form>', html)
        # Checking if member icon is present when user is not logged in
        self.assertIn('<img class="headicons" src="/static/purbeurre/assets/img/account_icon.png" alt="My Account">', html)
        # Checking if legal mentions are present and redirect to legal view
        self.assertIn('<a href="/purbeurre/legal" style="color: black;">Mentions légales</a>', html)


    def test_if_search_url_resolves_to_search_url(self):
        """ - Testing if 'Search' url points to 'Search' view """

        url = resolve('/purbeurre/search')
        self.assertEqual(url.func, search)


    def test_if_search_page_exists(self):
        """ - Tests if 'Search' view has corresponding template """

        # Retrieving search products
        fake_search_word = 'Produit1'
        fake_prd = Product.objects.using('purbeurre').get(name=fake_search_word)
        # Checking if status code is 200 ( - product found - )
        response = self.client.get(reverse('purbeurre:search'), {'search_word': fake_search_word})
        self.assertEqual(response.status_code, 200)
        # Checking if template used is 'result.html'
        self.assertTemplateUsed(response, 'purbeurre/result.html')


    def test_if_detail_url_resolves_to_detail_view(self):
        """ - Testing if 'Detail' url points to detail view """

        url = resolve('/purbeurre/detail/15')
        self.assertEqual(url.func, detail)


    def test_if_detail_page_exists(self):
        """ - Testing if 'Detail' view returns correct elements """

        # Retrieving one product with its id
        fake_prd_id = Product.objects.using('purbeurre').get(name="Produit1").id
        # Checking if status code is 200 (product found)
        response = self.client.get(reverse('purbeurre:detail', args=(fake_prd_id,)))
        self.assertEqual(response.status_code, 200)


    def test_saveprd_url_resolves_to_save_view(self):
        """ - Testing if 'Saveprd' url points to 'Saveprd' view """

        url = resolve('/purbeurre/saveprd/')
        self.assertEqual(url.func, saveprd)


    def test_product_is_saved(self):
        """ - Testing if a product is registered when user is logged in """

        # Counting elements before inserting a new product
        fav_count_before = Favourite.objects.using('purbeurre').count()
        # Retrieving required elements		
        fake_old_prd_barcode = Product.objects.using('purbeurre').get(name="Produit1").barcode
        fake_new_prd_barcode = Product.objects.using('purbeurre').get(name="Produit2").barcode
        fake_user = PbUser.objects.get(email="fake_email@adibou.com")
        # user is connected (returns True)		
        auth = self.client.login(username=fake_user, password="myPassword")
        # Testing if incoming request (from search view) can be sent to saveprd view		
        response = self.client.get(reverse('purbeurre:saveprd'), {
            'former_barcode': fake_new_prd_barcode,
            'new_barcode': fake_old_prd_barcode,
            'email': fake_user
        })
        # Counting elements after inserting a new product
        fav_count_after = Favourite.objects.using('purbeurre').count()
        # Testing if new favourite is added in Favourite DB
        self.assertEqual(fav_count_after, fav_count_before + 1)


    def test_showfavourites_url_resolves_to_showfavourites_view(self):
        """ - Testing if 'Showfavourites' url points to 'Showfavourites' view """

        url = resolve('/purbeurre/showfavourites')
        self.assertEqual(url.func, showfavourites)


    def test_showfavourites_contains_correct_elements(self):
        """ - Testing if 'Showfavourites' view returns correct elements """

        # Retrieving user email
        user = PbUser.objects.get(email="fake_email@adibou.com")
        # Authenticating user
        auth = self.client.login(username=user, password="myPassword")
        # Testing if response is ok for showfavourites view
        response = self.client.get(reverse('purbeurre:showfavourites'))
        self.assertEqual(response.status_code, 200)


    def test_if_account_url_resolves_to_account_view(self):
        """ - Testing if 'Account' url points to 'Account' view """

        url = resolve('/purbeurre/account')
        self.assertEqual(url.func, account)


    def test_if_account_page_exists(self):
        """ - Tests if 'Account' view has corresponding template"""

        # Getting connect url
        url = reverse('purbeurre:account')
        # Getting HttpResponse
        response = self.client.get(url)
        # Checking if 'Connect' view has an existing template
        self.assertEqual(response.status_code, 200)
        # Checking if template used is legal.html
        self.assertTemplateUsed(response, 'purbeurre/account.html')


    def test_if_connect_url_resolves_to_connect_view(self):
        """ - Testing if 'Connect' url points to 'Connect' view """

        url = resolve('/purbeurre/connect')
        self.assertEqual(url.func, connect)


    def test_if_connect_page_exists(self):
        """ - Tests if 'Connect' view has corresponding template"""

        # Getting connect url
        url = reverse('purbeurre:connect')
        # Getting HttpResponse
        response = self.client.get(url)
        # Checking if 'Connect' view has an existing template
        self.assertEqual(response.status_code, 200)
        # Checking if template used is legal.html
        self.assertTemplateUsed(response, 'purbeurre/connection.html')


    def test_if_disconnect_url_resolves_to_disconnect_view(self):
        """ Testing if 'Disconnect' url points to 'Disconnect' view """

        url = resolve('/purbeurre/disconnect')
        self.assertEqual(url.func, disconnect)


    def test_if_disconnect_page_exists(self):
        """ Tests if 'Disconnect' view has corresponding template """

        # Getting connect url
        url = reverse('purbeurre:disconnect')
        # Getting HttpResponse
        response = self.client.get(url)
        # Checking if 'Disconnect' view has an existing template
        self.assertEqual(response.status_code, 200)
        # Checking if template used is legal.html
        self.assertTemplateUsed(response, 'purbeurre/disconnection.html')


    def test_if_register_url_resolves_to_register_view(self):
        """ - Tests if 'Register' url points to 'Register' view """

        url = resolve('/purbeurre/register')
        self.assertEqual(url.func, register)


    def test_if_register_page_exists(self):
        """ - Tests if 'Register' view has corresponding template """

        # Counting nb of users before creating a new one
        user_count_before = PbUser.objects.count()
        # Creating a new fake user
        new_fake_user = PbUser.objects.create_user(
            username="Tony",
            email="myemail@gmail.com",
            password="myPassword"
        )
        # Testing if incoming request can be sent to register view
        response = self.client.get(reverse('purbeurre:register'))
        self.assertEqual(response.status_code, 200)
        # Counting elements after inserting a new product
        user_count_after = PbUser.objects.count()
        # Testing if new favourite is added in Favourite DB
        self.assertEqual(user_count_after, user_count_before + 1)


    def test_if_modifypassword_url_resolves_to_modifypassword_view(self):
        """ - Tests if 'Modifypassword' url points to 'Modifypassword' view """

        url = resolve('/purbeurre/modifypassword')
        self.assertEqual(url.func, modifypassword)


    def test_if_modifypassword_page_exists(self):
        """ - Test if 'Modifypassword' has corresponding template """

        # Checking if password can be changed
        fake_user = PbUser.objects.get(email='fake_email@adibou.com')
        fake_user.set_password("Mandibule")
        self.assertEquals(fake_user.check_password("Mandibule"), True)
        # Getting 'modifypassword' url
        url = reverse('purbeurre:modifypassword')
        # Getting HttpResponse
        response = self.client.get(url)
        # Checking if 'Modifypassword' view has an existing template
        self.assertEqual(response.status_code, 200)
        # Checking if template used is legal.html
        self.assertTemplateUsed(response, 'purbeurre/modifypassword.html')




