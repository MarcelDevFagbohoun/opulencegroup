from core.utils import SessionCart
from .models import Category, Cart, CartItem, Product, SiteInfo
from django.contrib.auth.models import AnonymousUser

def footer_categories(request):
    return {
        'footer_categories': Category.objects.filter(is_active=True)
    }

def get_or_create_cart(request):
    """
    Retourne le panier de l'utilisateur authentifié ou anonyme.
    Pour les anonymes, le panier est stocké en session.
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        # Créer un panier fictif à partir de la session
        session_cart = request.session.get('cart', {})
        # Objet cart temporaire pour template
        class SessionCart:
            def __init__(self, items):
                self.items = items

            @property
            def total_items(self):
                return sum(item['quantity'] for item in self.items)

            @property
            def total_price(self):
                return sum(item['total_price'] for item in self.items)

        # Transformer les données de session en objets compatibles
        items = []
        for product_id, data in session_cart.items():
            items.append(
                type('SessionCartItem', (), {
                    'product': type('ProductObj', (), {'id': int(product_id), 'name': data['name'], 'price': data['price']})(),
                    'quantity': data['quantity'],
                    'total_price': data['price'] * data['quantity']
                })()
            )
        return SessionCart(items)



def cart_context(request):
    cart = get_or_create_cart(request)
    if cart:
        cart_items = cart.items.all()  # ✅ must use .all()
        total_items = cart.total_items
        total_price = cart.total_price
    else:
        # Pour panier anonyme stocké en session
        session_cart = request.session.get('cart', {})
        cart_items = []
        for pid, data in session_cart.items():
            # Créer un objet fictif pour le template
            class AnonymousItem:
                def __init__(self, pid, data):
                    self.product = type("Prod", (), {"id": pid, "name": data['name'], "price": data['price'], "stock": 100, "image": None})()
                    self.quantity = data['quantity']
                    self.total_price = data['price'] * data['quantity']

            cart_items.append(AnonymousItem(pid, data))
        total_items = sum(item.quantity for item in cart_items)
        total_price = sum(item.total_price for item in cart_items)

    return {
        "cart": cart,
        "cart_items": cart_items,
        "cart_total_items": total_items,
        "cart_total_price": total_price,
    }
    
    
    
def site_info(request):
    """
    Fournit les informations globales du site à tous les templates.
    """
    site = SiteInfo.objects.first()  # On suppose un seul enregistrement
    return {
        'site_info': site
    }