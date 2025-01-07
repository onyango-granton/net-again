from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

# Choices for the Company model
SERVICE_CHOICES = (
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
)


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.username


@receiver(pre_save, sender=User)
def create_user_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.username)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.DateField()
    slug = models.SlugField(null=True)

    def age(self):
        today = date.today()
        age = today.year - self.birth.year - \
            ((today.month, today.day) < (self.birth.month, self.birth.day))
        return age

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("customer_profile", kwargs={"slug": self.slug})


@receiver(pre_save, sender=Customer)
def create_customer_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.user.username)


class Company(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    choices = SERVICE_CHOICES
    field = models.CharField(
        max_length=70, choices=choices, blank=False, null=False)

    slug = models.SlugField(null=True)

    def __str__(self):
        return str(self.user.id) + ' - ' + self.user.username

    def get_absolute_url(self):
        return reverse("company_profile", kwargs={"slug": self.slug})
