from django import forms

SERVICE_CHOICES = [
    ('', ''),
    ('Air Conditioner', 'Air Conditioner'),
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


class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, max_length=100, label='Description')
    price_hour = forms.DecimalField(
        decimal_places=2, max_digits=5, min_value=0.00)
    field = forms.ChoiceField(choices=SERVICE_CHOICES, required=True)

    def __init__(self, *args, choices=SERVICE_CHOICES, ** kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        if choices:
            self.fields['field'].choices = choices
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        self.fields['field'].widget.attrs['placeholder'] = 'Select Field of Work'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'

    def clean_field_of_work(self):
        data = self.cleaned_data['field']
        if data == '':
            raise forms.ValidationError("This field is required.")
        return data


class RequestServiceForm(forms.Form):
    address = forms.CharField(max_length=100)
    service_time = forms.DurationField()

    def __init__(self, *args, choices='', ** kwargs):
        super(RequestServiceForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Address'
        self.fields['service_time'].widget.attrs['placeholder'] = 'Enter Service Hours'
