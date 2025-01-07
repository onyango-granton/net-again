from django.contrib.auth import logout as django_logout
from django.db.models import Count
from django.shortcuts import render

from services.models import Service


def home(request):
    services = Service.objects.annotate(request_count=Count(
        'servicerequest')).order_by('-request_count')
    return render(request, "main/home.html", {"services": services})


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
