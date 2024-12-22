from django.urls import path
from . import views

urlpatterns = [
    path('register/customer', views.register_customer, name='register_customer'),
    path('register/company/',views.register_company, name='register_company'),
    path('services/', views.ServiceListView.as_view(), name='service_list')
]
