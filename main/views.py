import datetime
import json

from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from devrelhack.settings import db
from main.create_members import create_member, handle_uploaded_file, create_members
from main.diagrams import create_diagram
from main.templatetags.get import get_item


def index(request):
    return render(request, "base.html")


def table_view(request: HttpRequest):
    attributes = db.get_collection('attributes').find_one().get('attributes')
    db_members = db.get_collection('members')
    members = list(db_members.find())

    for attribute, meta in attributes.items():
        if meta.get('filter', 0) == 1:
            values = {get_item(member, attribute) for member in members}
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
                    if get_item(m, attribute) in values:
                        filtered_members.append(m)
                members = filtered_members
        table_html = ''
        for item in members:
            table_html += '<tr>\n'
            for header in attributes:
                table_html += f'<td>{get_item(item, header)}</td>\n'
            table_html += '</tr>'
        return JsonResponse({'table_html': table_html})
    return render(request, "table.html", {"data": members, "headers": attributes})


def create_member_view(request):
    attributes = db.get_collection('attributes').find_one().get('attributes')
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
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        valid_extensions = ['.csv', '.xls', '.xlsx']
        if not any(uploaded_file.name.endswith(i) for i in valid_extensions):
            print('error')
            return render(request, "import_members.html",
                          {'error': 'Неправильное расширение файла, поддерживаются только (.csv/.xls/.xlsx) '})
        print(uploaded_file)
        filename = f'{datetime.datetime.now()}-{uploaded_file.name}'
        handle_uploaded_file(uploaded_file, filename)
        res = create_members(filename)
        return render(request, 'import_members.html', res)
    return render(request, "import_members.html")


def get_analytics(request):
    attributes = db.get_collection("attributes").find_one().get("attributes")
    db_members = db.get_collection('members')
    members = list(db_members.find())
    fields = {}
    for k, meta in attributes.items():
        if meta.get('filter', 0) == 1:
            values = {get_item(member, k) for member in members}
            values = sorted(list(values))
            fields[k] = values

    if request.method == 'POST':
        field = request.POST.get('firstDropdown')
        filters = request.POST.getlist('filters')
        division_field = request.POST.get('thirdDropdown')
        filtered_members = list(db_members.find({field: {'$in': filters}}))
        categories = {}
        for member in filtered_members:
            specialization = member.get(division_field, '')
            if specialization in categories:
                categories[specialization].append(member)
            else:
                categories[specialization] = [member]
        filename = create_diagram(categories)
        return render(request, 'analytics.html', {'fields': fields, 'filename': filename})

    return render(request, 'analytics.html', {'fields': fields})


def mailing(request):
    print(request.method)
    return render(request, "mailing.html")


def download_data(request):
    if request.method == 'POST':
        try:
            attributes = list(db.get_collection("attributes").find_one().get("attributes").keys())
            data = request.POST.get('data')
            data = json.loads(data)
            csv_filename = "temp_data.csv"
            with open(csv_filename, "w") as csv_file:
                csv_file.write(';'.join(attributes) + '\n')
                for line in data:
                    csv_file.write(';'.join(line) + '\n')

            # Открываем и отправляем файл в ответе
            with open(csv_filename, 'rb') as csv_file:
                response = HttpResponse(csv_file.read(), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="data.csv"'
                return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
