from .models import Cart

def get_or_create_cart(request):
    """Retourne ou crée un panier selon user ou session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get("cart_id")
        if cart_id:
            cart = Cart.objects.filter(id=cart_id, user__isnull=True).first()
            if not cart:
                cart = Cart.objects.create()
                request.session["cart_id"] = cart.id
        else:
            cart = Cart.objects.create()
            request.session["cart_id"] = cart.id
    return cart




class SessionCart:
    """
    Panier pour utilisateur anonyme stocké dans la session.
    La structure de request.session['cart'] :
    {
        "product_id": {
            "name": str,
            "price": float,
            "quantity": int
        },
        ...
    }
    """
    def __init__(self, session):
        self.session = session
        self.cart = session.get('cart', {})

    @property
    def items(self):
        """Retourne une liste d'objets semblables à CartItem"""
        class Item:
            def __init__(self, product_id, data):
                self.product = type('Product', (), {})()
                self.product.id = int(product_id)
                self.product.name = data['name']
                self.product.price = data['price']
                self.quantity = data['quantity']

            @property
            def total_price(self):
                return self.product.price * self.quantity

        return [Item(pid, data) for pid, data in self.cart.items()]

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items)

    def add(self, product, quantity=1):
        pid = str(product.id)
        if pid in self.cart:
            self.cart[pid]['quantity'] += quantity
        else:
            self.cart[pid] = {'name': product.name, 'price': float(product.price), 'quantity': quantity}
        self.save()

    def update(self, product_id, quantity):
        pid = str(product_id)
        if pid in self.cart:
            self.cart[pid]['quantity'] = quantity
            self.save()

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True
