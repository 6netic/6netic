from django.http import HttpResponse
from .models import Category, Product, Favourite, PbUserManager, PbUser
from .forms import MemberForm, ConnectionForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.db import IntegrityError


def index(request):
    """ Homepage for purbeurre application """

    return render(request, 'purbeurre/index.html')


def legal(request):
    """ Redirects to legal mentions page """

    return render(request, 'purbeurre/legal.html')


def search(request):
    """ Finds a products the user is looking for """

    word = request.GET.get("search_word")
    # Retrieving the first product found
    try:
        search_prd = Product.objects.using('purbeurre').filter(name__icontains=word).first()
        search_prd_id = search_prd.id
        search_prd_nut = search_prd.nutrition_grade
        search_prd_cat = search_prd.prd_cat
        # Returns the first 6 products found
        best_prds = Product.objects.using('purbeurre').filter(prd_cat__exact=search_prd_cat). \
                        filter(nutrition_grade__lte=search_prd_nut). \
                        exclude(pk=search_prd_id)[:6]

        # Retrieves user email
        if request.user.is_authenticated:
            email = request.user.email
            favourites = Favourite.objects.using('purbeurre').all().filter(email_user=email)
            favourite_list = []
            for i in range(len(favourites)):
                new_code = favourites[i].favourite_barcode
                product = Product.objects.using('purbeurre').get(barcode=new_code).name
                favourite_list.append(product)

    except AttributeError:
        render(request, 'purbeurre/404.html')

    return render(request, 'purbeurre/result.html', locals())


def detail(request, product_id):
    """ Shows the detail of a specific food product """

    product = Product.objects.using('purbeurre').get(pk=product_id)
    context = {
        'product_name': product.name,
        'product_description': product.description,
        'product_nutrition_grade': product.nutrition_grade,
        'product_url': product.url,
        'product_url_pic': product.url_pic,
        'product_store': product.store,
        'product_fat': product.fat,
        'product_saturated_fat': product.saturated_fat,
        'product_sugar': product.sugar,
        'product_salt': product.salt,
    }
    return render(request, 'purbeurre/detail.html', context)


def saveprd(request):
    """ Saves a product into the database """

    former_barcode = request.GET.get("former_barcode")
    new_barcode = request.GET.get("new_barcode")
    email = request.user.email

    try:
        new_entry = Favourite.objects.using('purbeurre').create(
            former_barcode=former_barcode,
            favourite_barcode=new_barcode,
            email_user=email,
        )
        return HttpResponse(
            "<p align='center' style='color: green;'>Ce produit a bien été enregistré dans vos favoris</p>")
    except:
        return HttpResponse(
            "<p align='center' style='color: red;'>Ce produit a déjà été enregistré en base de données.</p>")


@login_required
def showfavourites(request):
    """ Shows all the registered products from a specific user """

    email = request.user.email
    favourites = Favourite.objects.using('purbeurre').all().filter(email_user=email)
    favourite_list = []
    for i in range(len(favourites)):
        new_code = favourites[i].favourite_barcode
        product = Product.objects.using('purbeurre').get(barcode=new_code)
        favourite_list.append(product)

    return render(request, 'purbeurre/favourite.html', locals())


def account(request):
    """ leads to member page """

    return render(request, 'purbeurre/account.html')


def register(request):
    """ This method is in charge of creating a new user in the database """

    form = MemberForm(request.POST or None)
    # Checking whether entered values from the formular are correct
    if form.is_valid():
        try:
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = PbUser.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            sending = 'ok'

        except IntegrityError:
            sending = 'nok'
        return render(request, 'purbeurre/register.html', locals())

    # if not in POST method then display the formular
    return render(request, 'purbeurre/register.html', locals())


def connect(request):
    """ This function connects a user to the system """

    # First access to connection form page
    if request.method == 'GET':
        redirection = request.GET.get('next')
    error = False

    if request.method == 'POST':
        form = ConnectionForm(request.POST)
        redirection = form["redirection"].value()

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)

                if redirection != 'None':
                    return redirect(redirection)
            else:
                error = True
    else:
        form = ConnectionForm()

    return render(request, 'purbeurre/connection.html', locals())


def disconnect(request):
    """ Disconnects a user to the system """

    logout(request)
    return render(request, 'purbeurre/disconnection.html', locals())


def modifypassword(request):
    """ Modifies user's password """

    # This is a POST request so we need to process the form data
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                former_password = form.cleaned_data['old_password']
                new_password1 = form.cleaned_data['new_password1']
                new_password2 = form.cleaned_data['new_password2']

                if request.user.check_password(former_password):
                    if new_password1 == new_password2:
                        #print(request.user.email)
                        u = PbUser.objects.get(email=request.user.email)
                        u.set_password(new_password2)
                        u.save()

                        return render(request, 'purbeurre/passwordmodified.html')

                    else:
                        # Only former password is correct
                        resp = "onlyformer"

                else:
                    # Former password is false and new password is not the same in both fields
                    resp = "none"

            except:
                # Datas transmitted cannot be taken into account
                resp = "data_error"

            return render(request, 'purbeurre/modifypassword.html', locals())

    else:
        # First time the form is loaded
        form = ChangePasswordForm()

    return render(request, 'purbeurre/modifypassword.html', {'form': form})





