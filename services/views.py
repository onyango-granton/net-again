from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CreateNewService, RequestServiceForm
from .models import SERVICE_CHOICES, Service, ServiceRequest


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    user = request.user

    if not user.is_authenticated or not hasattr(user, 'company'):
        messages.error(request, "You are not associated with a company.")
        return render(request, 'services/create.html')

    if user.company.field != "All in One":
        company_field = [(user.company.field, user.company.field)]
    else:
        company_field = SERVICE_CHOICES

    if request.method == "POST":
        form = CreateNewService(request.POST, choices=company_field)
        if form.is_valid():
            name, description, price_hour, field = (form.cleaned_data[key] for key in [
                                                    "name", "description", "price_hour", "field"])

            Service.objects.create(
                name=name,
                description=description,
                price_hour=price_hour,
                field=field,
                company=user.company
            )

            messages.success(request, 'Service created successfully.')
            return redirect('/services')
        else:
            messages.error(
                request, 'There was an error creating the service. Please check the form and try again.')
    else:
        form = CreateNewService(choices=company_field)

    return render(request, 'services/create.html', {"form": form})


def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    user = request.user
    form = RequestServiceForm(request.POST or None)

    if request.method != "POST":
        return render(request, 'services/request_service.html', {"form": form})

    if not form.is_valid():
        messages.error(
            request, 'There was an error with your submission. Please check the form and try again.')
        return render(request, 'services/request_service.html', {"form": form})

    if not user:
        messages.error(request, "You are not associated with a company.")
        return render(request, 'services/request_service.html', {"form": form})

    address = form.cleaned_data["address"]
    service_time = form.cleaned_data["service_time"]
    service = get_object_or_404(Service, id=id)

    new_service_request = ServiceRequest(
        service=service,
        user=user,
        address=address,
        service_time=service_time
    )
    new_service_request.save()

    messages.success(request, 'Service request submitted successfully.')
    return redirect('/services')
