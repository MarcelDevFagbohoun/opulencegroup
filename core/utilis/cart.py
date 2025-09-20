# utils/cart.py
from decimal import Decimal

def get_cart(request):
    """
    Retourne le panier de l'utilisateur (auth ou session)
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = [{
            'id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'total_price': float(item.total_price)
        } for item in cart.items.all()]
        total_price = float(cart.total_price)
    else:
        session_cart = request.session.get('cart', {})
        items = []
        total_price = 0
        for product_id, data in session_cart.items():
            total = data['price'] * data['quantity']
            total_price += total
            items.append({
                'id': int(product_id),
                'name': data['name'],
                'price': data['price'],
                'quantity': data['quantity'],
                'total_price': total
            })
    return {'items': items, 'total_price': total_price}
