from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('profile/', views.profile, name='profile'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('orders/', views.orders, name='orders'),
    path('faq/', views.faq, name='faq'),
    path('receipt/', views.receipt, name='receipt'),
    path('receipt/<str:order_number>/', views.receipt, name='receipt_detail'),
]
