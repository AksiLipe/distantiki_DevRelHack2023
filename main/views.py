from bson import ObjectId
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from devrelhack.settings import db
from main.create_members import create_member


def index(request):
    return render(request, "base.html")


def table_view(request: HttpRequest):
    attributes = {'Почта': {'unique': 1, 'filter': 0}, 'Номер Телефона': {'unique': 1, 'filter': 0},
                  'Имя': {'unique': 0, 'filter': 0}, 'Фамилия': {'unique': 0, 'filter': 0},
                  'Телеграм': {'unique': 1, 'filter': 0},
                  'Стаж': {'unique': 0, 'filter': 1},
                  'Специализация': {'unique': 0, 'filter': 1}}
    members = [{'_id': ObjectId('657cb67287d6f3db2363a86c'), 'Почта': 'ilmirsharifullin2000@gmail.com', 'Имя': 'Ilmir',
                'Фамилия': 'Sharifullin', 'Номер Телефона': 79520367755, 'Телеграм': 'dedailmir',
                'Специализация': 'backend',
                'Стаж': '1-3 года'},
               {'_id': ObjectId('657cb82180271735dfeff498'), 'Почта': 'qwerty@example.com', 'Имя': 'Вадим',
                'Фамилия': 'Филиппов',
                'Номер Телефона': 7987654321, 'Специализация': 'backend', 'Стаж': '1-3 года'},
               {'_id': ObjectId('657d5db27ea97f66a6694068'), 'Имя': 'Дима', 'Почта': 'asdfgh@gmail.com',
                'Телеграм': 'dedadima'},
               {'_id': ObjectId('657d5e310ce084be218c9d67'), 'Почта': 'zxc@example.com', 'Имя': 'Иван',
                'Фамилия': 'Иванов',
                'Номер Телефона': 79876543210, 'Телеграм': 'qwerty123', 'Специализация': 'frontend', 'Стаж': '<1 года'}]
    for attribute, meta in attributes.items():
        if meta.get('filter', 0) == 1:
            values = {member.get(attribute, '') for member in members}
            meta['select'] = sorted(list(values))
            attributes[attribute] = meta

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        filters = request.GET.dict()
        for attribute, values in filters.items():
            if values:
                values = values[1:].split(';')
                filtered_members = []
                for m in members:
                    if m.get(attribute, '') in values:
                        filtered_members.append(m)
                members = filtered_members
        table_html = ''
        for item in members:
            table_html += '<tr>\n'
            for header in attributes:
                table_html += f'<td>{item.get(header, "")}</td>\n'
            table_html += '</tr>'
        return JsonResponse({'table_html': table_html})
    return render(request, "table.html", {"data": members, "headers": attributes})


def create_member_view(request):
    attributes = {'Почта': {'unique': 1, 'filter': 0}, 'Номер Телефона': {'unique': 1, 'filter': 0},
                  'Имя': {'unique': 0, 'filter': 0}, 'Фамилия': {'unique': 0, 'filter': 0},
                  'Телеграм': {'unique': 1, 'filter': 0},
                  'Стаж': {'unique': 0, 'filter': 1},
                  'Специализация': {'unique': 0, 'filter': 1}}
    if request.method == "POST":
        data = {}
        for field_name in attributes:
            data[field_name] = request.POST.get(field_name)

        res = create_member(data)
        if res:
            return redirect('table-view')
        else:
            return render(request, "add_member.html",
                          {"fields": attributes, 'error': 'Используются уникальные поля разных пользователей'})
    else:
        return render(request, "add_member.html", context={"fields": attributes})


def import_members(request):
    return render(request, "import_members.html")

def mailing(request):
    return render(request, "mailing.html")