from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_company = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
class ServiceField(models.TextChoices):
    AIR_CONDITIONER = 'AIR', 'Air Conditioner'
    ALL_IN_ONE = 'ALL', 'All in One'
    CARPENTRY = 'CAR', 'Carpentry'
    ELECTRICITY = 'ELE', 'Electricity'
    GARDENING = 'GAR', 'Gardening'
    HOME_MACHINES = 'HOM', 'Home Machines'
    HOUSEKEEPING = 'HOU', 'Housekeeping'
    INTERIOR_DESIGN = 'INT', 'Interior Design'
    LOCKS = 'LOC', 'Locks'
    PAINTING = 'PAI', 'Painting'
    PLUMBING = 'PLU', 'Plumbing'
    WATER_HEATERS = 'WAT', 'Water Heaters'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username
    
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    field_of_work = models.CharField(
        max_length = 3,
        choices = ServiceField.choices
    )

    def __str__(self):
        return self.user.username
    
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    field = models.CharField(
        max_length=3
        choices=[(k,v) for k,v in ServiceField if k != 'ALL']
    )
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')

    def clean(self):
        if self.company.field_of_work != 'ALL' and self.company.field_of_work != self.field:
            raise ValidationError("Service field must match company's field of work")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date-created']

    def __str__(self):
        return self.name