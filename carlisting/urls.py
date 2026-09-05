from django.urls import path

from . import views

app_name = 'carlisting'

urlpatterns = [
    path('', views.home, name='home'),
    path('inventory/', views.car_list, name='car_list'),
    path('inventory/<int:pk>/', views.car_detail, name='car_detail'),
    path('contact/', views.contact, name='contact'),
]
