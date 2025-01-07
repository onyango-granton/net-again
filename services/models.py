from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.db import models

from users.models import Company, User

from .forms import SERVICE_CHOICES


class Service(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    choices = SERVICE_CHOICES
    field = models.CharField(
        max_length=30,
        choices=choices,
        blank=False,
        null=False
    )
    date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    service_time = models.DurationField()
    choices = SERVICE_CHOICES
    field = models.CharField(max_length=30,  choices=choices)
    date = models.DateTimeField(auto_now=True, null=False)
