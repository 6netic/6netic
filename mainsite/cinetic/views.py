from django.shortcuts import render


def homepage(request):
    """ Homepage of 6netic website """

    return render(request, "cinetic/index.html")


def projets(request):
    """ Projects section """

    return render(request, "cinetic/projets.html")


def services(request):
    """ Services section """

    return render(request, "cinetic/services.html")


def contact(request):
    """ Contact section """

    return render(request, "cinetic/contact.html")