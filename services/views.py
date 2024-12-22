from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerRegistrationForm, ServiceRequestForm,ServiceForm,CompanyRegistratioForm
from django.contrib.auth import login
from django.views.generic import ListView, DetailView
from .models import Service
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your views here.
def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration/register_customer.html', {'form':form})

def register_company(request):
    if request.method == 'POST':
        form = CompanyRegistratioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CompanyRegistratioForm()
    return render(request, 'registration/register_company.html', {'form':form})

class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'

class ServiceCategoryListView(ListView):
    model = Service
    template_name = 'services/service_category_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(field=self.kwargs['field'])
    
class PopularServicesView(ListView):
    model = Service
    template_name = 'services/popular_services.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.annotate(
            request_count = Count('requests')
        ).order_by('-request_count')[:10]
    
@login_required
def profile_view(request):
    user = request.user
    if user.is_company:
        services = user.company.services.all()
        return render(request, 'profiles/company_profile.html',{'services':services})
    else:
        service_requests = user.customer.service_requests.all()
        return render(request, 'profiles/customer_profile.html', {'service_requests': service_requests})
    
@login_required
def create_service(request):
    if not request.user.is_company:
        messages.error(request, "Only companies can create services")
        return redirect('home')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.company = request.user.company
            try:
                service.save()
                return redirect('service_detail', pk=service.pk)
            except ValidationError as e:
                form.add_error(None, e.message)
    else:
        form = ServiceForm()
    return render(request, 'services/create_service.html', {'form':form})

@login_required
def request_service(request, service_id):
    if request.user.is_company:
        messages.error(request, "Companies cannot request services")
        return redirect('home')
    
    if not hasattr(request.user, 'customer'):
        messages.error(request, "You must create a customer profile to request for a service")
        return redirect('profile')
    
    service = get_object_or_404(Service, pk=service_id)

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.service = service
            service_request.customer = request.user.customer
            service_request.save()
            return redirect('profile')
    else:
        form = ServiceRequestForm()

    return render(request, 'services/request_service.html', {'form':form, 'service':service})