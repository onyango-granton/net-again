from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer, ServiceField, Company

class CustomerRegistrationForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = False
        if commit:
            user.save()
        Customer.objects.create(
            user = user,
            date_of_birth = self.cleaned_data['date_of_birth']
        )
        return user
    
class CompanyRegistratioForm(UserCreationForm):
    field_of_work = forms.ChoiceField(choices=ServiceField.choices)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        if commit:
            user.save()
        Company.objects.create(
            user = user,
            field_of_work = self.cleaned_data['field_of_work']
        )
        return user
    
    