from django.shortcuts import render, HttpResponse


def index(request):
    """ Index page of ciblerie application """

    return render(request, "ciblerie/index.html")


def ten_meters(request):
    """ view for ten meters category """

    return render(request, "ciblerie/ten_meters.html")

def tests_1(request):
    """ view for tests 1 category """

    return render(request, "ciblerie/tests_1.html")

def tests_2(request):
    """ view for tests 2 category """

    return render(request, "ciblerie/tests_2.html")