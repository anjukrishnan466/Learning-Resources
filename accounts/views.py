import io
from urllib import request

import xlwt
from chartjs.views.lines import BaseLineChartView
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import login as authlogin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.http import (FileResponse, Http404, HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import TemplateView
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
# from tablib import Dataset
from xhtml2pdf import pisa

from resources.models import Category, Resources, Status, TimeSpendUser

# from resources.forms import TimeSpendCreate


# Create your views here.
# To show user home page.

@login_required(login_url='account_login')
def home(request):
    resources = Resources.objects.all()
    resources_count = Resources.objects.count()
    users = User.objects.all()
    user_count = User.objects.count()
    open_count = Status.objects.filter(status=0, user_id=request.user).count()
    in_progress = Status.objects.filter(status=1, user_id=request.user).count()
    closed = Status.objects.filter(status=2, user_id=request.user).count()
    return render(request, 'accounts/home.html', {'resources': resources, 'resources_count': resources_count, 'users': users, 'user_count': user_count, 'open_count': open_count, 'in_progress': in_progress, 'closed': closed})


@login_required(login_url='login')
# To show user index page.
def index(request):
    accounts = User.objects.filter(is_superuser='False').order_by('id')

    return render(request, 'accounts/index.html', {'accounts': accounts})
# To show user login page.


def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:

            authlogin(request, user)
            request.session['logged_in'] = True

            return render(request, 'accounts/home.html')
        else:

            messages.error(request, "invalid user name or password")
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

# To show user register page.


def register(request):

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "username already exist")
                return redirect('/accounts/register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "email already exist")
                return redirect('/accounts/register')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, "user successfully created")
                return redirect('/accounts/login')

        else:
            messages.error(request, "password not matching")
            return redirect('/accounts/register')

    else:

        return render(request, 'accounts/register.html')
# for show user logout.


def logout(request):
    auth.logout(request)
    return redirect('/accounts/login')


@login_required(login_url='login')
# To show user add page.
def store(request):

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "username already exist")
                return redirect('store')
            elif User.objects.filter(email=email).exists():
                messages.error(request, "email already exist")
                return redirect('store')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, "user successfully created")
                return redirect('/accounts/index')

        else:
            messages.error(request, "password not matching")
            return redirect('store')

    else:

        return render(request, 'accounts/form.html')
# To show user edit page.


@login_required(login_url='login')
def edit(request, id):
    accounts = User.objects.get(id=id)
    if request.method == 'POST':
        accounts.first_name = request.POST['first_name']
        accounts.last_name = request.POST['last_name']
        accounts.username = request.POST['username']
        accounts.email = request.POST['email']
        accounts.password1 = request.POST['password1']
        accounts.password2 = request.POST['password2']
        accounts.save()
        messages.success(request, "user successfully created")
        return redirect('/accounts/index')

    else:
        accounts = User.objects.get(id=id)
        return render(request, 'accounts/edit_form.html', {'accounts': accounts})
# To show user delete page.


@login_required(login_url='login')
def delete(request, id):
    accounts = User.objects.get(id=id)
    accounts.delete()
    return redirect('/accounts/index')
# To show resources list according to user


def resourceIndex(request, id):
    accounts = User.objects.get(id=id)

    resources = Resources.objects.filter(User__id=id)
    return render(request, 'resources/resourcelist.html', {'resources': resources})

# To show resources details according to user


@login_required(login_url='account_login')
def accountsResources(request, id):
    resources = Resources.objects.get(id=id)
    status = Status.objects.get(user_id=request.user.id, resources_id=id)
    timespend = TimeSpendUser.objects.filter(status_id=status.id)

    return render(request, 'resources/resourcedetailsuser.html', {"resources": resources, 'status': status, 'id': id, 'timespend': timespend})
# To download uploaded file


@login_required(login_url='login')
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
# To edit status of resource by user


@login_required(login_url='account_login')
def status_edit(request, id):
    if request.method == 'POST':

        resources = Resources.objects.get(id=id)
        statusdata = Status.objects.get(
            user_id=request.user.id, resources_id=id)
        statusdata.status = request.POST['status']
        statusdata.total_time_spend = statusdata.total_time_spend + \
            int(request.POST['time_spend'])
        statusdata.save()
        date_user = request.POST['date']

        time_spend_user = request.POST['time_spend']

        TimeSpendUser.objects.create(
            date_user=date_user, time_spend_by_user=time_spend_user, status=statusdata)
        return redirect(f'/accounts/accountsResources/{id}')

# To provide serch in user index


@login_required(login_url='login')
def search_accounts(request):
    search_query = request.GET['search']
    data = User.objects.filter(Q(first_name__icontains=search_query))

    return render(request, 'accounts/index.html', {'accounts': data})
# To provide serch in resource index


@login_required(login_url='login')
def search_resourcelist(request):
    search_query = request.GET['search']
    data = Resources.objects.filter(Q(title__icontains=search_query))
    return render(request, 'resources/resourcelist.html', {'resources': data})

# To show resources details according to user for admin


@login_required(login_url='account_login')
def assigned_resources(request, id):
    accounts = User.objects.get(id=id)

    resources = Resources.objects.filter(User__id=id)
    return render(request, 'accounts/resourcelist.html', {'resources': resources, 'user_id': id})

# To show resources details according to user for admin


@login_required(login_url='account_login')
def accountsResources_admin(request, id, user_id):
    resources = Resources.objects.get(id=id)
    status = Status.objects.get(user_id=user_id, resources_id=id)
    timespend = TimeSpendUser.objects.filter(status_id=status.id)

    return render(request, 'accounts/resourcedetailsuser.html', {"resources": resources, 'status': status, 'id': id, 'timespend': timespend})

# bulk upload of userdata


@login_required(login_url='login')
def upload_user(request):
    if "GET" == request.method:
        return render(request, 'accounts/index1.html', {})
    else:
        new_persons = request.FILES['myfile']
        dataset = Dataset()
        imported_data = dataset.load(new_persons.read(), format='xlsx')
        print(imported_data)
        for data in imported_data:
            print(data)
            value = User(
                first_name=data[0],
                last_name=data[1],
                username=data[2],
                email=data[3],
                password=make_password('123456')
            )
            value.save()

        return redirect('/accounts/index')

# download all user data


@login_required(login_url='login')
def download_user(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    # this will make a sheet named Users Data
    ws = wb.add_sheet('Resources Data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['First Name', 'Last Name', 'User Name', 'Email', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.filter(is_superuser='False').values_list(
        'first_name', 'last_name', 'username', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

# status of resources


class LineChartJSONView(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        resources = Status.objects.all().filter.distinct(
            'resources_id').select_related('resources')
        final_results = []
        for resource in resources:
            I = resource.resources.title
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

# pdf download-resource learning progress of user


@login_required(login_url='login')
def progress(request, id):

    resources = Resources.objects.filter(User__id=id)

    for resource in resources:

        status = Status.objects.filter(
            user_id=id, resources_id=resource.id)

        for stat in status:
            timespend = TimeSpendUser.objects.filter(status_id=stat.id)

    return render(request, 'accounts/progress.html', {'resources': resources})

# pdf download-all resource learning progress of user


def user_pdf(request, id):
    # Create a file-like buffer to receive PDF data.
    buf = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    lines = [

    ]
    inner_lines = []

    accounts = User.objects.get(id=id)

    resources = Resources.objects.filter(User__id=id)
    data = []
    for resource in resources:
        const_resource = {}

        const_resource['resources'] = "Resource : " + str(resource.title)
        status = Status.objects.get(
            user_id=id, resources_id=resource.id)

        timespend = TimeSpendUser.objects.filter(status_id=status.id)
        line = []
        for timesp in timespend:
            inner_lines = {}

            inner_lines['date_user'] = "Date : "+str(timesp.date_user)
            inner_lines['time_spend_by_user'] = "Time Spend : " + \
                str(timesp.time_spend_by_user)
            line.append(inner_lines)

        const_resource['timesp'] = line
        data.append((const_resource))
    for dat in data:
        textob.textLine((dat['resources']))
        for value in dat['timesp']:
            textob.textLine(str(value['date_user']))

            textob.textLine(str(value['time_spend_by_user']))
        textob.textLine("---------------")

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='user_progress.pdf')

# pdf download-one resource learning progress of user


@login_required(login_url='adminlogin')
def user_progress(request, id, user_id):
    template_path = 'accounts/resource_progress_pdf.html'
    resources = Resources.objects.get(id=id)
    status = Status.objects.get(user_id=user_id, resources_id=id)
    timespend = TimeSpendUser.objects.filter(status_id=status.id)
    context = {"resources": resources, 'status': status,
               'id': id, 'timespend': timespend}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
