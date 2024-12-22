from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm
from django.contrib.auth import login

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