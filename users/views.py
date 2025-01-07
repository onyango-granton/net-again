from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from .forms import CompanySignUpForm, CustomerSignUpForm, UserLoginForm
from .models import Company, Customer, User


def register(request):
    return render(request, 'users/register.html')


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            user.save()

            customer_profile = Customer(
                user=user, birth=form.cleaned_data['date_of_birth']
            )
            customer_profile.save()

            user.customer_profile = customer_profile
            user.save()

            login(self.request, user)
            return redirect('/')
        else:
            return self.form_invalid(form)


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_company = True
        user.save()

        company_profile = Company(
            user=user, field=form.cleaned_data['field_of_work'])
        company_profile.save()

        user.company_profile = company_profile
        user.save()

        login(self.request, user)
        return redirect('/')


def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_company:
                    company = Company.objects.get(user=user)
                    company.save()
                if user.is_customer:
                    customer = Customer.objects.filter(user=user).first()
                    customer.save()
                return redirect('/')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})
