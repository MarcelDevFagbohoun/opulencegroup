from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def shop(request):
    return render(request, 'core/shop.html')

def category(request, slug):
    return render(request, 'core/category.html', {'category_slug': slug})

def search(request):
    return render(request, 'core/search.html')

def product_detail(request, slug):
    return render(request, 'core/product_detail.html', {'product_slug': slug})

def cart(request):
    return render(request, 'core/cart.html')

def checkout(request):
    return render(request, 'core/checkout.html')

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

def profile(request):
    return render(request, 'core/account/profile.html')

def wishlist(request):
    return render(request, 'core/account/wishlist.html')

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

