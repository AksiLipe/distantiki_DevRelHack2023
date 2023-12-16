from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from devrelhack.settings import db
from main.create_members import create_member


def index(request):
    return render(request, "base.html")


def table_view(request: HttpRequest):
    attributes = db.get_collection("attributes").find_one().get("attributes")
    db_members = db.get_collection('members')
    members = list(db_members.find())
    for attribute, meta in attributes.items():
        if meta.get('filter', 0) == 1:
            values = {member.get(attribute, '') for member in members}
            meta['select'] = values
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
    attributes = db.get_collection("attributes").find_one().get("attributes")
    cursor = db.get_collection("members").find()
    members = list(cursor)
    if request.method == "POST":
        data = {}
        for field_name in attributes:
            data[field_name] = request.POST.get(field_name)

        res = create_member(data)
        if res:
            return HttpResponse("Данные успешно добавлены!")
        else:
            return render(request, "add_member.html",
                          {"fields": attributes, 'error': 'Используются уникальные поля разных пользователей'})
    else:
        return render(request, "add_member.html", {"fields": attributes})


def import_table_view(request):
    pass
