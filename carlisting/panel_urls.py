from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'panel'

urlpatterns = [
    path('login/', views.PanelLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='panel:login'), name='logout'),
    path('', views.panel_dashboard, name='dashboard'),

    path('cars/', views.panel_car_list, name='car_list'),
    path('cars/new/', views.panel_car_create, name='car_create'),
    path('cars/<int:pk>/edit/', views.panel_car_edit, name='car_edit'),
    path('cars/<int:pk>/delete/', views.panel_car_delete, name='car_delete'),

    path('brands/', views.panel_brand_list, name='brand_list'),
    path('brands/<int:pk>/delete/', views.panel_brand_delete, name='brand_delete'),

    path('inquiries/', views.panel_inquiry_list, name='inquiry_list'),
    path('inquiries/<int:pk>/toggle/', views.panel_inquiry_toggle, name='inquiry_toggle'),
]
