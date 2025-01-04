from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Company, Customer

User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'

def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(f"{value} is already taken.")

class CustomerSignUpForm(UserCreationForm):
    birth = forms.DateField(required=False, widget=DateInput())
    email = forms.EmailField(
        max_length=100,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'birth', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data.get('email')
        user.save()
        customer = Customer.objects.create(
            user=user,
            birth=self.cleaned_data.get('birth')
        )
        return user

class CompanySignUpForm(UserCreationForm):
    field = forms.ChoiceField(choices=(
        ('Air Conditioner', 'Air Conditioner'),
        ('All in One', 'All in One'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters')
    ))
    email = forms.EmailField(
        max_length=100,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'field', 'password1', 'password2')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data.get('email')
        user.save()
        company = Company.objects.create(
            user=user,
            field=self.cleaned_data.get('field')
        )
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Email', 'autocomplete': 'off'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)