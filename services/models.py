from django.db import models
from django.contrib.auth.models import AbstractUser

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

