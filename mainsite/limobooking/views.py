import os
import dotenv
from django.shortcuts import render
from django.shortcuts import redirect
from .compute_days import *
from .models import Booking
from .forms import ReservationForm, SearchForm
from decimal import Decimal

dotenv.load_dotenv(os.path.join('.env'))

def homepage(request):
    """ Homepage of the application """

    home = True
    return render(request, 'cinetic/index.html', locals())


def index(request):
    """ Index of the application, first access to the app """

    return render(request, "limobooking/index.html")


def home(request):
    """ Homepage of the application """

    return render(request, "limobooking/home.html")


def aeroports(request):
    """ Homepage of the application """

    return render(request, "limobooking/aeroports.html")


def gares(request):
    """ Homepage of the application """

    return render(request, "limobooking/gares.html")


def otherDestination(request):
    """ Homepage of the application """

    googleApiKey = os.getenv("GOOGLE_API_KEY")
    if request.method == 'GET':
        # destination is sent via GET method
        if (request.GET.get("destination")):
            destination = request.GET.get("destination")
            return redirect('limobooking:displayJourney', destination=destination)
        # This is the first access to autreDestination page
        else:
            form = ReservationForm()
            return render(request, "limobooking/autredestination.html", locals())


def displayJourney(request, destination):
    """ View for displaying empty form in destinations.html page """

    googleApiKey = os.getenv("GOOGLE_API_KEY")
    # This is the first time we access the page with destination value given
    if request.method == 'GET':
        form = ReservationForm()
        return render(request, "limobooking/destinations.html", locals())


def selectJourney(request):
    """ Selecting required date and time """

    googleApiKey = os.getenv("GOOGLE_API_KEY")
    if request.method == 'POST':
        # User has selected the destination, date, time, sharing and personal information
        form = ReservationForm(request.POST)
        if form.is_valid():
            hour = form.cleaned_data['hour']
            minutes = form.cleaned_data['minute']
            departureTime = hour + ':' + minutes
            destination = form.cleaned_data['destination']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            compute = Compute(
                form.cleaned_data['departureDate'], hour,
                form.cleaned_data['sharing'], float(request.POST.get("distance"))
            )
            prixCourse, departureDate, sharing = compute.calculate_individual_price()
            # Looking for other bookings
            try:
                bookings_in_base = Booking.objects.using('limobooking').filter(departureDate__exact=departureDate)\
                    .filter(sharing__exact=sharing).filter(destination__exact=destination)
                if bookings_in_base:
                    prices_dict = compute.compute_grouped_price(bookings_in_base)
                else:
                    onlyOne = True
            except:
                pass
            return render(request, "limobooking/destinations.html", locals())


def recordJourney(request):
    """ Records values in the database """

    if request.method == 'POST':
        destination = request.POST.get("destination")
        departureDate = request.POST.get('departureDate')
        departureTime = request.POST.get("departureTime")
        sharing = request.POST.get("sharing")
        lastname = request.POST.get("lastname")
        firstname = request.POST.get("firstname")
        email = request.POST.get("email")
        prixCourse = Decimal(request.POST.get('prixCourse').replace(',', '.'))
        # Register booking into database
        if request.POST.get("validation"):
            try:
                newBooking = Booking.objects.using('limobooking').create(
                    destination=destination,
                    departureDate=departureDate,
                    departureTime=departureTime,
                    sharing=sharing,
                    lastname=lastname,
                    firstname=firstname,
                    email=email,
                    price=prixCourse,
                )
                messageOk = "Réservation enregistrée"
                message = True
            except:
                messageNok = "Vous avez déjà effectué une réservation à cette date pour cette destination"
                message = True
            return render(request, "limobooking/record.html", locals())
        return render(request, "limobooking/record.html", locals())


def cancelJourney(request):
    """ Cancels a booking from the database """

    if request.method == 'GET':
        if request.GET.get("email"):
            email = request.GET.get("email")
            departureDate = request.GET.get("departureDate")
            try:
                cancel = Booking.objects.using('limobooking').filter(email__contains=email)\
                                .filter(departureDate=departureDate)
                if cancel:
                    return render(request, "limobooking/cancel.html", locals())
                else:
                    message = "Aucune réservation trouvée à cette date"
                    return render(request, "limobooking/cancel.html", locals())
            except:
                pass
        first = True
        form = SearchForm()
        return render(request, "limobooking/cancel.html", locals())

    if request.method == 'POST':
        id = request.POST.get("id")
        try:
            delete = Booking.objects.using('limobooking').filter(pk=id).delete()
            messDel = "La réservation a bien été annulée. Merci de votre confiance."
        except:
            pass
        return render(request, "limobooking/cancel.html", locals())


