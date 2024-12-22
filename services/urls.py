from django.urls import path
from . import views

urlpatterns = [
    path('register/customer', views.register_customer, name='register_customer'),
    path('register/company/',views.register_company, name='register_company'),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/category/<str:field>/', views.ServiceCategoryListView.as_view(), name='service_category')
]
