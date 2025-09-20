from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
      
    
]
