from django.http import HttpResponse
from django.shortcuts import render

from devrelhack.settings import db


def index(request):

    return render(request, 'base.html')


def create_members_view(request):
    attributes = db.get_collection('attributes').find_one().get('attributes')
    cursor = db.get_collection('members').find()
    members = list(cursor)
    print(attributes)
    print(members)
    if request.method == 'POST':
        data = {
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "telegram": request.POST.get("telegram"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            # Добавьте другие поля, если они предоставлены в форме
        }
        return HttpResponse('Данные успешно добавлены!')
    else:

        return render(request, 'your_template.html')


def table_view(request):
    attributes = db.get_collection('attributes').find_one().get('attributes')
    cursor = db.get_collection('members').find()
    members = list(cursor)
    return render(request, 'table.html', context={'headers': attributes, 'data': members})
