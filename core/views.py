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

from core.context_processors import get_or_create_cart
from core.utils import SessionCart
from .models import CartItem, Category, Product, Review, UserProfile, Cart, Wishlist
from .forms import NewsletterForm, RegisterForm, LoginForm, UserProfileForm
import re




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redirige vers la page d'accueil
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
            return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('home')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect('home')

        user = User.objects.create_user(username=email, email=email, password=password1,
                                        first_name=first_name, last_name=last_name)
        user.save()
        login(request, user)
        return redirect('home')


def home(request):
    # Get categories (optional)
    categories = Category.objects.all()[:6]

    # Get best-selling or featured products
    # Example: featured products (you can create a field 'is_best_seller')
    best_sellers = Product.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:6]
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:3]

    for product in best_sellers:
        product.rounded_rating = round(product.average_rating or 0)
    newsletter_form = NewsletterForm(request.POST or None)
    
    if request.method == "POST":
        if newsletter_form.is_valid():
            newsletter_form.save()
            messages.success(request, "You have successfully subscribed!")
            return redirect('home')  # Redirect to clear POST
    
    else:
        form = NewsletterForm()

    context = {
        'reviews':reviews,
        'categories': categories,
        'best_sellers': best_sellers,
        'newsletter_form':newsletter_form,
    }
    return render(request, 'core/home.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    qty = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = item.quantity + qty if not created else qty
        item.save()
    else:
        session_cart = SessionCart(request.session)
        session_cart.add(product, qty)

    return redirect('cart_detail')


def update_cart_item(request, product_id):
    qty = int(request.POST.get('quantity', 1))
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.quantity = qty
        item.save()
    else:
        session_cart = SessionCart(request.session)
        session_cart.update(product_id, qty)

    return redirect('cart_detail')


def remove_cart_item(request, product_id):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        item.delete()
    else:
        session_cart = SessionCart(request.session)
        session_cart.remove(product_id)

    return redirect('cart_detail')

def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, "core/cart.html", {"cart": cart})


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


@login_required
def wishlist_view(request):
    """Afficher la wishlist de l'utilisateur"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, "core/user/wishlist.html", {"wishlist": wishlist})
@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, "core/user/wishlist.html", {"wishlist": wishlist})

@login_required
def clear_wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.clear()
    return redirect("wishlist")  # renvoie vers la page favoris


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        return JsonResponse({"status": "removed"})
    else:
        wishlist.products.add(product)
        return JsonResponse({"status": "added"})
    

@login_required
def remove_from_wishlist(request, product_id):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wishlist.products.remove(product)
    return redirect('wishlist')  # redirige vers la page wishlist

    
def checkout(request):
    return render(request, 'core/checkout.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Order, Wishlist, Cart

@login_required
def profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    wishlist, _ = Wishlist.objects.get_or_create(user=user)
    cart, _ = Cart.objects.get_or_create(user=user)
    orders = Order.objects.filter(user=user).order_by('-created_at')[:5]

    if request.method == 'POST':
        # Update user info
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        profile.city = request.POST.get('city', profile.city)
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'core/user/profile.html', {
        'user': user,
        'profile': profile,
        'wishlist': wishlist,
        'cart': cart,
        'orders': orders,
    })
    

def order_confirmation(request):
    return render(request, 'core/order_confirmation.html')

def about(request):
    return render(request, 'core/pages/about.html')

def contact(request):
    return render(request, 'core/pages/contact.html')

def blog(request):
    return render(request, 'core/pages/blog.html')

def blog_detail(request, slug):
    return render(request, 'core/pages/blog_detail.html', {'article_slug': slug})


def orders(request):
    return render(request, 'core/account/orders.html')

def faq(request):
    return render(request, 'core/pages/faq.html')

def receipt(request, order_number=None):
    # In a real application, you would fetch the order from the database
    # order = Order.objects.get(order_number=order_number)
    context = {
        'order_number': order_number or 'ORD-2024-001'
    }
    return render(request, 'core/receipt.html', context)



