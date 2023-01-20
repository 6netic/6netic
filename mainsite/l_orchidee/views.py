from django.contrib.auth import authenticate, login, logout
from . forms import ConnectForm, ChangePasswordForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from . process import Process
from . prepare import Prepare
from . models import Tour, Nurse, PlanningModel
from . check_vars import check_vars, verify_date, check_planning
from django.http import JsonResponse
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from django_globals import globals
from os import listdir, remove
from django.views.generic.list import ListView
from . planning_tour import PlanningTour
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


def clean_db(request):
    """ Clears all databases """

    Tour.objects.using('lorchidee').all().delete()
    PlanningModel.objects.using('lorchidee').all().delete()
    return redirect(reverse('l_orchidee:index'))


def index(request):
    """ Index page accessible only if logged in """

    # if request.user.is_authenticated:
    #     return render(request, "l_orchidee/index.html")
    # else:
    #     return redirect(reverse('l_orchidee:connect'))
    return render(request, "l_orchidee/index.html")

##########################   Tour Section   ####################################

# @login_required
def display_form(request):
    """ Inserts 2 tours for a specific date  """

    context = {}
    context['nurses'] = Nurse.objects.using('lorchidee').all()
    return render(request, 'l_orchidee/display_form.html', context=context)


# @login_required
def check_variables(request):
    """ Checks whether all variables are correct """

    eval_obj = check_vars(request)
    if isinstance(eval_obj, list):
        return render(request, "l_orchidee/display_detailed_form.html",
                      context={'bad_var': eval_obj, 'show_btn': True})
    else:
        globals.tours = Prepare(
            eval_obj['date_tour'], eval_obj['tour_name1'], eval_obj['tour_name2'],
            eval_obj['nurse1'], eval_obj['nurse2'])
        globals.tours.createFolders()
        globals.tours.saveOnLocal([eval_obj['pdf_file1'], eval_obj['pdf_file2']])
        globals.tours.converPdf2Jpg(eval_obj['pdf_file1'].name, "l_orchidee/documents/prefecture/")
        globals.tours.converPdf2Jpg(eval_obj['pdf_file2'].name, "l_orchidee/documents/village/")
        globals.tours.del_pdf_files()
        # Defining global variables to store dates and lines for next methods
        globals.all_dates, globals.all_lines = [], []
        message = ["Fichiers pdf convertis en image jpg.", "Extraction des fichiers dans le dossier Préfecture..."]
        return render(request, "l_orchidee/display_detailed_form.html", context={'converted': message})


# @login_required
def extract_in_pref(request):
    """ Extracts in prefecture folder """

    dir = "l_orchidee/documents/prefecture/"
    if len(listdir(dir)) != 0:
        files_list = sorted(listdir(dir), key=lambda x: int(x[-5:-4]))
        if int(files_list[0][-5:-4]) == 0:
            date, lines = Process().extractText(dir, files_list[0], globals.tours.nurse1, globals.tours.tour_name1)
            globals.all_dates.append(date)
        else:
            lines = Process().extractText(dir, files_list[0], globals.tours.nurse1, globals.tours.tour_name1)
        for one in lines:
            globals.all_lines.append(one)
        message = "Le fichier : " + files_list[0] + " a été extrait"
        remove("l_orchidee/documents/prefecture/" + files_list[0])
        return render(request, "l_orchidee/display_detailed_form.html", context={'pref_extracting': message})
    message = "Extraction des fichiers dans le dossier village..."
    return render(request, "l_orchidee/display_detailed_form.html", context={'pref_extracted': message})


# @login_required
def extract_in_vill(request):
    """ Extracts in village folder """

    dir = "l_orchidee/documents/village/"
    if len(listdir(dir)) != 0:
        files_list = sorted(listdir(dir), key=lambda x: int(x[-5:-4]))
        if int(files_list[0][-5:-4]) == 0:
            date, lines = Process().extractText(dir, files_list[0], globals.tours.nurse2, globals.tours.tour_name2)
            globals.all_dates.append(date)
        else:
            lines = Process().extractText(dir, files_list[0], globals.tours.nurse2, globals.tours.tour_name2)
        for one in lines:
            globals.all_lines.append(one)
        message = "Le fichier : " + files_list[0] + " a été extrait"
        remove("l_orchidee/documents/village/" + files_list[0])
        return render(request, "l_orchidee/display_detailed_form.html", context={'vill_extracting': message})
    message = "Vérification de la validité de la date et si la tournée n'est pas déjà présente en BDD..."
    return render(request, "l_orchidee/display_detailed_form.html", context={'vill_extracted': message})


# @login_required
def check_date_and_is_registered(request):
    """ Checks validity of date and if tour is already in the database """

    date_list = Process().convertDate(globals.all_dates)
    check_date = verify_date(globals.tours.date_tour, date_list)
    if isinstance(check_date, list):
        return render(request, "l_orchidee/display_detailed_form.html",
                      context={'error_in_date': check_date, 'show_btn': True})
    # Checking if date is already in the database
    saved_tour_pref = Tour.objects.using('lorchidee').filter(jour=globals.tours.date_tour).filter(nomTournee="Préfecture")
    saved_tour_vill = Tour.objects.using('lorchidee').filter(jour=globals.tours.date_tour).filter(nomTournee="Le Village")
    if saved_tour_pref and saved_tour_vill:
        message = "A cette date, les 2 tournées ont déjà été enregistrées !"
        return render(request, "l_orchidee/display_detailed_form.html",
                      context={'already_in': message, 'show_btn': True})
    else:
        message = "Enregistrement en base de données..."
        return render(request, "l_orchidee/display_detailed_form.html", context={'recording_status': message})


# @login_required
def insert_tour(request):
    """ Inserts datas into the database """

    for line in globals.all_lines:
        new_entry = Tour.objects.using('lorchidee').create(
            nurse=Nurse.objects.using('lorchidee').get(id=int(line[7])),
            jour=globals.tours.date_tour,
            heure=line[0],
            patient=line[1],
            addrTel=line[2],
            cotation=line[3],
            assure=line[4],
            honoraire=line[5],
            finTraitement=line[6],
            commentaires="",
            nomTournee=line[8]
        )
    message = "Enregistrement de ces tournées effectué avec succès !"
    return render(request, "l_orchidee/display_detailed_form.html", context={'recorded': message})


# @login_required
def display_tour(request):
    """ Displays a tour for a selected date """

    if request.method == 'POST':
        context = {}
        if not request.POST.get("date_search"):
            return render(request, "l_orchidee/display_detailed_tour.html", context={'no_date': True})
        if not request.POST.get("nom_tournee"):
            tour_name = "Préfecture"
        else:
            tour_name = escape(request.POST.get("nom_tournee"))
        context['tour_name'] = tour_name
        date = escape(request.POST.get("date_search"))
        context['date'] = date
        tour_day = Tour.objects.using('lorchidee').filter(jour=date).filter(nomTournee=tour_name).order_by('id')
        if tour_day:
            context['tour_day'] = tour_day
            return render(request, "l_orchidee/display_detailed_tour.html", context=context)
        else:
            context['no_tour'] = True
            return render(request, "l_orchidee/display_detailed_tour.html", context=context)
    # GET method
    return render(request, "l_orchidee/display_tour.html", context={'calendar': True})


# @login_required
def save_comment(request):
    """ Saves a comment for a specific line """

    if request.method == 'POST':
        try:
            this_id = int(request.POST.get("this_id"))
            comment = escape(request.POST.get("comment_content"))
            entry = Tour.objects.using('lorchidee').get(pk=this_id)
            entry.commentaires = comment
            entry.save()
            return JsonResponse(status=200, data={'message': "Ok"})
        except:
            return JsonResponse(status=230, data={'message': "Not Ok"})


# @login_required
def validate_line(request):
    """ Validates selected line """

    if request.method == 'POST':
        try:
            this_id = int(request.POST.get("this_id"))
            entry = Tour.objects.using('lorchidee').get(pk=this_id)
            entry.traite = True
            entry.save()
            return JsonResponse(status=200, data={'message': "Ok"})
        except:
            return JsonResponse(status=230, data={'message': "Not OK"})


##########################   Planning Section   ####################################

class PlanningView(ListView):
    """ Custom view class for the planning """

    model = PlanningModel
    template_name = 'l_orchidee/view_planning.html'

    def get_context_data(self, **kwargs):
        """ Renvoie les données du contexte pour afficher la liste des objects """

        context = super().get_context_data(**kwargs)
        date_object = get_date(self.request.GET.get('year'), self.request.GET.get('month'))
        context['previous_year'] = get_previous_month(date_object)[0]
        context['previous_month'] = get_previous_month(date_object)[1]
        context['next_year'] = get_next_month(date_object)[0]
        context['next_month'] = get_next_month(date_object)[1]
        # Instanciate Calendar class
        planning = PlanningTour(date_object.year, date_object.month)
        context['show_planning'] = mark_safe(planning.display_month())
        # Calculates occurences
        context['nurses'] = Nurse.objects.using('lorchidee').all()
        context['ramata_pref'] = PlanningModel.objects.using('lorchidee').filter(dateTour__year=date_object.year).\
            filter(dateTour__month=date_object.month).filter(tour1=1)
        context['ramata_vill'] = PlanningModel.objects.using('lorchidee').filter(dateTour__year=date_object.year). \
            filter(dateTour__month=date_object.month).filter(tour2=1)
        context['amaria_pref'] = PlanningModel.objects.using('lorchidee').filter(dateTour__year=date_object.year). \
            filter(dateTour__month=date_object.month).filter(tour1=2)
        context['amaria_vill'] = PlanningModel.objects.using('lorchidee').filter(dateTour__year=date_object.year). \
            filter(dateTour__month=date_object.month).filter(tour2=2)
        context['beatrice_pref'] = PlanningModel.objects.using('lorchidee').filter(dateTour__year=date_object.year). \
            filter(dateTour__month=date_object.month).filter(tour1=3)
        context['beatrice_vill'] = PlanningModel.objects.using('lorchidee').filter(dateTour__year=date_object.year). \
            filter(dateTour__month=date_object.month).filter(tour2=3)
        context['sonia_pref'] = PlanningModel.objects.using('lorchidee').filter(dateTour__year=date_object.year). \
            filter(dateTour__month=date_object.month).filter(tour1=4)
        context['sonia_vill'] = PlanningModel.objects.using('lorchidee').filter(dateTour__year=date_object.year). \
            filter(dateTour__month=date_object.month).filter(tour2=4)
        return context


def get_date(the_year, the_month):

    if the_year and the_month:
        try:
            the_year, the_month = int(the_year), int(the_month)
            return date(the_year, the_month, 1)
        except:
            print("There has been an error with year and, or month")
    return datetime.now()


def get_previous_month(date_object):

    previous_month = date(date_object.year, date_object.month, 1) - timedelta(days=1)
    year, month = previous_month.year, previous_month.month
    return year, month


def get_next_month(date_object):
    next_month = date(date_object.year, date_object.month, 1) + relativedelta(months=1)
    year, month = next_month.year, next_month.month
    return year, month


# @login_required
def insert_planning(request):
    """ Inserts a new tour for one day from the calendar """

    context = {}
    if request.method == 'POST':
        eval_obj = check_planning(request)
        if isinstance(eval_obj, list):
            context['bad_var'] = eval_obj
            return render(request, "l_orchidee/insert_planning_resp.html", context=context)
        else:
            date_planning = eval_obj['date_tour']
            nurse_tour_pref = eval_obj['nurse1_tour_pref']
            nurse_tour_vill = eval_obj['nurse2_tour_vill']
            rec_confirm = eval_obj['rec_confirm']
            already_in = PlanningModel.objects.using('lorchidee').filter(dateTour=date_planning)
            if already_in and rec_confirm != 'yes':
                context['in_db'] = True
                context['entry'] = already_in
                return render(request, "l_orchidee/insert_planning_resp.html", context=context)
            PlanningModel.objects.using('lorchidee').filter(dateTour=date_planning).delete()
            PlanningModel.objects.using('lorchidee').create(
                dateTour=date_planning,
                tour1=Nurse.objects.using('lorchidee').get(id=int(nurse_tour_pref)),
                tour2=Nurse.objects.using('lorchidee').get(id=int(nurse_tour_vill)))
            context['registered'] = "Cette date est bien enregistrée."
            return render(request, "l_orchidee/insert_planning_resp.html", context=context)

    context['nurses'] = Nurse.objects.using('lorchidee').all()
    return render(request, 'l_orchidee/insert_planning.html', context=context)

##########################   Member Section   ####################################

def connect(request):
    """ Connects a user to the system """

    if request.method == 'POST':
        form = ConnectForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('l_orchidee:index'))
            else:
                error = True
    else:
        form = ConnectForm()
    return render(request, 'l_orchidee/viewConnect.html', locals())


# @login_required
def disconnect(request):
    """ Disconnects a user to the system """

    logout(request)
    form = ConnectForm()
    return render(request, "l_orchidee/viewConnect.html", locals())


# @login_required
def modifyPassword(request):
    """ Modifies user's password """

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                former_password = form.cleaned_data['old_password']
                new_password1 = form.cleaned_data['new_password1']
                new_password2 = form.cleaned_data['new_password2']
                if request.user.check_password(former_password):
                    if new_password2 == new_password1:
                        current_user = User.objects.get(username=request.user.username)
                        current_user.set_password(new_password2)
                        current_user.save()
                        return render(request, "l_orchidee/modifyPassword.html", {'resp_ok': True})
                    else:
                        # Only former password is correct
                        resp = "only_former"
                else:
                    # Former password is false and new password is not the same in the two fields
                    resp = "none_of_them"
            except:
                # Data sent cannot be taken into account
                resp = "error_in_data"
            return render(request, "l_orchidee/modifyPassword.html", locals())
    else:
        # First time form is loaded
        form = ChangePasswordForm()
        return render(request, "l_orchidee/modifyPassword.html", {'form': form, 'resp': True})

