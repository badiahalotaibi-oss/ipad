from django.urls import path

from . import views


app_name = 'menu'

urlpatterns = [
    path('', views.home, name='home'),
    path('cashier/menu-screen/', views.home, name='cashier_menu_screen'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
]
