from django.shortcuts import render

from devrelhack.settings import db


def index(request):

    return render(request, 'base.html')