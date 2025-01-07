from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_date_of_birth(value):
    if value >= date.today() or value.year < 1900 or value.year > 2005:
        raise ValidationError('Invalid date of birth.')


class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Enter Date of Birth (DD-MM-YYYY)',
        validators=[validate_date_of_birth]
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',
                  'email', 'date_of_birth')

    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter same password'
        for field in self.fields.values():
            field.widget.attrs['autocomplete'] = 'off'


FIELD_OF_WORK_CHOICES = [
    ('', ''),
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
    ('Water Heaters', 'Water Heaters'),
]


class CompanySignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    field_of_work = forms.ChoiceField(
        choices=FIELD_OF_WORK_CHOICES,
        required=True,
        widget=forms.Select(attrs={'placeholder': 'Select Field of Work'}),
        label='Field of Work'
    )

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}
    ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',
                  'email', 'field_of_work')

    def __init__(self, *args, **kwargs):
        super(CompanySignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Re-enter same password'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        for field in self.fields.values():
            field.widget.attrs['autocomplete'] = 'off'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already taken.")
        return email

    def clean_field_of_work(self):
        data = self.cleaned_data['field_of_work']
        if data == '':
            raise forms.ValidationError("This field is required.")
        return data


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        max_length=30,
        widget=forms.TextInput(
            attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
