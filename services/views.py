from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm, CompanyRegistratioForm
from django.contrib.auth import login
from django.views.generic import ListView, DetailView
from .models import Service
from django.db.models import Count

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