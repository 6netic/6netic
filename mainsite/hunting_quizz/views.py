from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from . forms import add_question_form
from . models import Hunting, Response
from . utils import update_list, assisted_update_list
from django.utils.html import escape
import random
from django.http import HttpResponse

def index(request):
    """ Homepage view """

    return render(request, 'hunting_quizz/index.html')


def apprentissage(request):
    """ Apprentissage view """

    return render(request, 'hunting_quizz/apprentissage.html')


def normal_quizz(request):
    """ Normal quizz view """

    picture_id = random.choice([1, 2, 3])
    # Answer submitted by user
    if request.GET.get('ids_list'):
        question_id, ids_list = update_list(request)
        option_ans = escape(request.GET.get('options'))
        current_question_nb = int(request.GET.get('current_question_nb')) + 1
        nb_of_questions = int(request.GET.get('nb_of_questions'))
        time_spent = int(request.GET.get('stop_time'))
        # important = escape(request.GET.get('important')) # type to be checked
        record_answer = Response.objects.using('huntingquizz').create(
            quest=Hunting.objects.using('huntingquizz').get(id=question_id),
            usranswer=option_ans
        )
        # No more questions left, results will be calculated
        if len(ids_list) == 0:
            score = 0
            all_resp = Response.objects.using('huntingquizz').all()
            for one in all_resp:
                # print(one.quest.answer)
                if one.usranswer == one.quest.answer:
                    score += 1
            percent = round((score / nb_of_questions) * 100)
            wrong = nb_of_questions - score
            return render(request, 'hunting_quizz/results.html', locals())
        # Other questions to display
        questions = Hunting.objects.using('huntingquizz').filter(pk__in=ids_list)
        return render(request, 'hunting_quizz/normal_quizz.html', locals())
    # First access to the page
    else:
        # nb_of_questions is the total number of questions
        nb_of_questions = 3
        current_question_nb = 1
        time_spent = 0
        Response.objects.using('huntingquizz').all().delete()
        all_questions = Hunting.objects.using('huntingquizz').all().count()
        iterat = 1
        ids_list = []
        while iterat <= nb_of_questions:
            i = random.randint(1, all_questions)
            if i not in ids_list:
                ids_list.append(i)
                iterat += 1
        questions = Hunting.objects.using('huntingquizz').filter(pk__in=ids_list)
        return render(request, 'hunting_quizz/normal_quizz.html', locals())


def assisted_quizz(request):
    """ vue assistee """

    picture_id = random.choice([1, 2, 3])
    score = 0
    if request.POST.get('ids_list'):
        question_id, ids_list = assisted_update_list(request)
        option_ans = escape(request.POST.get('options'))
        current_question_nb = int(request.POST.get('current_question_nb')) + 1
        nb_of_questions = int(request.POST.get('nb_of_questions'))
        score = int(request.POST.get('score'))
        current_question = Hunting.objects.using('huntingquizz').\
            filter(id=question_id).values_list('answer', 'ansdesc', 'important')
        if option_ans == current_question[0][0]:
            score += 1
            reponse = "Bonne réponse."
        else:
            reponse = "Mauvaise réponse."
        if current_question[0][2] == True:
            eliminatoire = "Il s'agit d'une question éliminatoire !"
        else:
            eliminatoire = ""
        if len(ids_list) == 0:
            last = True
        else:
            last = False
        return JsonResponse(status=200, data={
           "reponse": reponse,
            "explications": current_question[0][1],
            "eliminatoire": eliminatoire,
            "score": score,
            "last": last
        })

    if request.GET.get('ids_list'):
        question_id, ids_list = update_list(request)
        current_question_nb = int(request.GET.get('current_question_nb')) + 1
        nb_of_questions = int(request.GET.get('nb_of_questions'))
        score = int(request.GET.get('score'))
        questions = Hunting.objects.using('huntingquizz').filter(pk__in=ids_list)
        if len(ids_list) == 0:
            percent = round((score / nb_of_questions) * 100)
            wrong = nb_of_questions - score
            return render(request, 'hunting_quizz/results.html', locals())
        return render(request, 'hunting_quizz/assisted_quizz.html', locals())

    # nb_of_questions is the total number of questions
    nb_of_questions = 3
    current_question_nb = 1
    Response.objects.using('huntingquizz').all().delete()
    all_questions = Hunting.objects.using('huntingquizz').all().count()
    iterat = 1
    ids_list = []
    while iterat <= nb_of_questions:
        i = random.randint(1, all_questions)
        if i not in ids_list:
            ids_list.append(i)
            iterat += 1
    questions = Hunting.objects.using('huntingquizz').filter(pk__in=ids_list)
    return render(request, 'hunting_quizz/assisted_quizz.html', locals())


def add_question(request):

    if request.method == 'POST':
        form = add_question_form(request.POST)
        if form.is_valid():
            new_entry = Hunting.objects.using('huntingquizz').create(
                question=form['question'].value(),
                choice1=form['choice1'].value(),
                choice2=form['choice2'].value(),
                choice3=form['choice3'].value(),
                imgdir=form['imgdir'].value(),
                answer=form['answer'].value(),
                ansdesc=form['ansdesc'].value(),
                important=form['important'].value()
            )
            return redirect(reverse('hunting_quizz:index'))

    form = add_question_form()
    return render(request, 'hunting_quizz/add_question.html', locals())

