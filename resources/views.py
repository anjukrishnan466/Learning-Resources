import json
import os
from django.db.models import Count
from operator import countOf
from typing import Counter

import xlwt
from chartjs.views.lines import BaseLineChartView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from tablib import Dataset

from resources.models import Status

from .forms import GenerateRandomUserForm, ResourcesCreate
from .models import Resources
from .tasks import import_excel

# Create your views here.
# To show admin home page.


@login_required(login_url='login')
def home(request):
    resources = Resources.objects.all()
    resources_count = Resources.objects.count()
    user = User.objects.all()
    user_count = User.objects.count()

    open_count = Status.objects.filter(status=0).count()

    in_progress = Status.objects.filter(status=1).count()
    closed = Status.objects.filter(status=2).count()

    return render(request, 'resources/home.html', {'resources': resources, 'resources_count': resources_count, 'user': user, 'user_count': user_count, 'open_count': open_count, 'in_progress': in_progress, 'closed': closed})
# To show resource list page.


@login_required(login_url='login')
def index(request):
    resources = Resources.objects.all().order_by('id')
    return render(request, 'resources/index.html', {'resources': resources})
# To show resources add page.


@login_required(login_url='login')
def store(request):
    if request.method == 'POST':
        form = ResourcesCreate(request.POST, request.FILES)
        if form.is_valid():
            ResourcesCreate(request.FILES['resource_file'])
            form.save()
            return redirect('/resources/index')
    else:
        form = ResourcesCreate()

    return render(request, "resources/entry.html", {
        "form": form
    })
# To show resources delete page.


@login_required(login_url='login')
def delete(request, id):
    resources = Resources.objects.get(id=id)
    resources.delete()
    return redirect('/index')
# To show resources edit page.


@login_required(login_url='login')
def edit(request, id):
    resources = Resources.objects.get(id=id)
    form = ResourcesCreate(request.POST or None, instance=resources)
    if request.method == 'POST':
        form = ResourcesCreate(request.POST, request.FILES, instance=resources)
        if (request.FILES.get('resource_file')):
            ResourcesCreate(request.FILES.get('resource_file'))

        print(form.is_valid())

        if form.is_valid():
            form.save()

        return redirect('/resources/index')

    else:
        return render(request, 'resources/entry1.html', {"form": form, "id": id})
# To assign resources to user page.


@login_required(login_url='login')
def assign(request, id):
    user_with_resource = []
    user_all = []
    all_user = []
    resources = Resources.objects.get(id=id)
    accounts = User.objects.filter(is_superuser='False')
    if request.method == 'POST':
        users_checks = request.POST.getlist('check')
        for check in users_checks:
            resources.User.add(check)

            resources.save()
        return redirect('/resources/index')

    else:
        resources = Resources.objects.get(id=id)
        checked = Status.objects.filter(resources_id=id).all()

        for check in checked:
            I = check.user_id
            # print(user_with_resource)

            user_with_resource.append(I)
        for account in accounts:
            J = account.id
            # print(user_all)

            user_all.append(J)

        user_without_resource = (set(user_all)) - (set(user_with_resource))
        for user_without in user_without_resource:
            k = User.objects.get(id=user_without)
            all_user.append(k)

        return render(request, 'resources/assignUser.html', {'resources': resources, 'accounts': accounts, 'all_user': all_user})
# To show resources details page.


@login_required(login_url='login')
def resourcesView(request, id):

    resources = Resources.objects.get(id=id)

    return render(request, 'resources/details.html', {"resources": resources})
# To download uploaded file page.


def download(request, id):
    resources = Resources.objects.get(id=id)

    file_path = os.path.join(settings.MEDIA_ROOT, resources.resource_file.path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    raise Http404
# To provide search in index page.


@login_required(login_url='login')
def search_products(request):
    search_query = request.GET['search']
    data = Resources.objects.filter(Q(title__icontains=search_query))

    return render(request, 'resources/index.html', {'resources': data})

# chart for resource status
class LineChartJSONView(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        resources = Status.objects.all().distinct(
            'resources_id').select_related('resources')
        final_results = []
        for resource in resources:
            I = resource.resources.title
            print(I)
            final_results.append(I)
        return final_results

    def get_providers(self):
        """Return names of datasets."""
        return ["Open", "Inprogress", "Closed"]

    def get_data(self):
        """Return 3 datasets to plot."""
        resources = Status.objects.all().distinct('resources_id')
        open_status = []
        progress = []
        closed = []

        for resource in resources:
            I = resource.resources_id
            status_open = Status.objects.filter(
                status=0, resources_id=I).count()
            status_progress = Status.objects.filter(
                status=1, resources_id=I).count()
            status_closed = Status.objects.filter(
                status=2, resources_id=I).count()

            open_status.append(status_open)
            progress.append(status_progress)
            closed.append(status_closed)

        return [open_status,
                progress,
                closed]


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

# bulk upload of resources
@login_required(login_url='login')
def upload_resources(request):
    if "GET" == request.method:
        return render(request, 'resources/upload.html', {})
    else:

        myfile = request.FILES['myfile']
        dataset = Dataset()
        imported_data = dataset.load(myfile.read(), format='xlsx')

        import_excel.delay(imported_data.export('json'))

        return redirect('/resources/index')

# download all resource data 
@login_required(login_url='login')
def download_resources(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="resources.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    # this will make a sheet named Users Data
    ws = wb.add_sheet('Resources Data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Title', 'Description', 'Link', 'Resource_file', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Resources.objects.all().values_list(
        'title', 'description', 'link', 'resource_file')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response
