from django.shortcuts import get_object_or_404, render

from services.models import Service, ServiceRequest
from users.models import Company, User


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    user = get_object_or_404(User, slug=name)
    user_service_requests = ServiceRequest.objects.filter(
        user=user).order_by("-id")

    for service_request in user_service_requests:
        service_request.total_price = float(
            service_request.service.price_hour) * service_request.service_time.total_seconds()

    return render(request, "users/profile.html", {"user": user, 'services': user_service_requests})


def company_profile(request, name):
    user = get_object_or_404(User, slug=name)
    services = Service.objects.filter(
        company=Company.objects.get(user=user)).order_by("-date")

    return render(request, 'users/profile.html', {'user': user, 'services': services})
