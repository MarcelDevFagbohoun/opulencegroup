from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import *
import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ContactForm

def home(request):
    # Get categories (optional)
    categories = Category.objects.all()[:6]
    services = Service.objects.filter(is_active=True)
    # Get best-selling or featured products
    # Example: featured products (you can create a field 'is_best_seller')
    best_sellers = Product.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:6]
    hero_slides = HeroSlide.objects.filter(is_active=True)

    
    context = {
        'services':services,
        'hero_slides':hero_slides,
        'categories': categories,
        'best_sellers': best_sellers,
    }
    return render(request, 'core/home.html', context)



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Ajouter les produits similaires (même catégorie)
    similar_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'core/product_detail.html', context)



def shop(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Récupérer les catégories sélectionnées depuis GET
    selected_categories = request.GET.getlist('category')  # ici on peut l’envoyer au template

    # Filtrage par catégorie
    if selected_categories:
        products = products.filter(category__slug__in=selected_categories)

    # Filtrage par prix
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)

    context = {
        'products': products,
        'categories': categories,
        'selected_categories': selected_categories,  # ✅ à utiliser dans le template
        'price_min': price_min,
        'price_max': price_max,
    }
    return render(request, 'core/shop.html', context)


    

def about(request):
    return render(request, 'core/pages/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre message a été envoyé avec succès !")
            return redirect('contact')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'core/contact.html',context)

