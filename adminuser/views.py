from chartjs.views.lines import BaseLineChartView
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import login as authlogin
from django.contrib.auth import logout
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from resources.models import Resources, Status

# Create your views here.

# To show login for admin page.


def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        # if user is not None:
        if user.is_superuser:
            authlogin(request, user)
            request.session['logged_in'] = True
            return redirect('/adminuser/home')
        else:
            messages.error(request, "invalid user name or password")
            return redirect('/adminuser/login')
    else:
        return render(request, 'adminuser/login.html')
# To show logout for admin page.


def logout(request):

    auth.logout(request)
    return redirect('/adminuser/login')

# To show index for admin.


def index(request):

    resources = Resources.objects.all()
    resources_count = Resources.objects.count()
    users = User.objects.all()
    user_count = User.objects.count()
    open_count = Status.objects.filter(status=0).count()
    in_progress = Status.objects.filter(status=1).count()
    closed = Status.objects.filter(status=2).count()
    data = {'resources_count': resources_count, 'open_count': open_count,
            'in_progress': in_progress, 'closed': closed}

    return render(request, 'adminuser/home.html', {'resources': resources, 'resources_count': resources_count, 'users': users, 'user_count': user_count, 'open_count': open_count, 'in_progress': in_progress, 'closed': closed, 'data': data})


def home(request):
    resources = Resources.objects.all()
    resources_count = Resources.objects.count()
    users = User.objects.all()
    user_count = User.objects.count()
    open_count = Status.objects.filter(status=0).count()
    in_progress = Status.objects.filter(status=1).count()
    closed = Status.objects.filter(status=2).count()
    return render(request, 'adminuser/home.html', {'resources': resources, 'resources_count': resources_count, 'users': users, 'user_count': user_count, 'open_count': open_count, 'in_progress': in_progress, 'closed': closed})
