from django.http import HttpResponse
from django.shortcuts import render
from devrelhack.settings import db
from main.create_members import create_member


def index(request):
    return render(request, "base.html")


def table_view(request):
    attributes = db.get_collection("attributes").find_one().get("attributes")
    cursor = db.get_collection("members").find()
    members = list(cursor)
    print(attributes)
    print(members)
    data = [
        {"_id": "657cb67287d6f3db2363a86c", "Почта": "ilmirsharifullin2000@gmail.com", "Имя": "Ilmir",
         "Фамилия": "Sharifullin", "Номер Телефона": 79520367755, "Телеграм": "dedailmir"},
        {"_id": "657cb82180271735dfeff498", "Почта": "qwerty@example.com", "Имя": "Вадим", "Фамилия": "Филиппов",
         "Номер Телефона": 7987654321},
        {"_id": "657d5db27ea97f66a6694068", "Имя": "Дима", "Почта": "asdfgh@gmail.com", "Телеграм": "dedadima"},
        {"_id": "657d5e310ce084be218c9d67", "Почта": "zxc@example.com", "Имя": "Иван", "Фамилия": "Иванов",
         "Номер Телефона": 79876543210, "Телеграм": "qwerty123"}
    ]

    headers = {
        "Почта": {"unique": 1, "filter": 0},
        "Номер Телефона": {"unique": 1, "filter": 0},
        "Имя": {"unique": 0, "filter": 0},
        "Фамилия": {"unique": 0, "filter": 0},
        "Телеграм": {"unique": 1, "filter": 0},
        "Стаж": {"unique": 0, "filter": 1},
        "Специализация": {"unique": 0, "filter": 1}
    }
    headers = headers.keys()
    return render(request, "table.html", {"data": data, "headers": headers})


def create_member_view(request):
    attributes = db.get_collection("attributes").find_one().get("attributes")
    cursor = db.get_collection("members").find()
    members = list(cursor)
    print(attributes)
    print(members)
    if request.method == "POST":
        data = {}
        for field_name in attributes:
            data[field_name] = request.POST.get(field_name)

        res = create_member(data)
        if res:
            return HttpResponse("Данные успешно добавлены!")
        else:
            return render(request, "add_member.html", {"fields": attributes, 'error': 'Используются уникальные поля разных пользователей'})
    else:
        return render(request, "add_member.html", {"fields": attributes})
