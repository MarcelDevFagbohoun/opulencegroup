from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


# ------------------------
# E-COMMERCE
# ------------------------

class Category(models.Model):
    """Catégorie de produits"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Produit"""
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = RichTextField(verbose_name="Description")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    image = models.ImageField(upload_to='products/', verbose_name="Image")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_featured = models.BooleanField(default=False, verbose_name="Vedette")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        return self.stock > 0 and self.is_active

    @property
    def average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        return reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0


class Order(models.Model):
    """Commande"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('processing', 'En traitement'),
        ('shipped', 'Expédiée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Livraison
    delivery_name = models.CharField(max_length=100, verbose_name="Nom complet")
    delivery_phone = models.CharField(max_length=20, verbose_name="Téléphone")
    delivery_address = models.TextField(verbose_name="Adresse de livraison")

    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande #{self.id} - {self.user.username}"

    @property
    def order_number(self):
        return f"CMD{self.id:06d}"


class OrderItem(models.Model):
    """Article d'une commande"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Article de commande"
        verbose_name_plural = "Articles de commande"

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.price * self.quantity


class Cart(models.Model):
    """Panier"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Panier"
        verbose_name_plural = "Paniers"

    def __str__(self):
        return f"Panier de {self.user.username}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Article du panier"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article du panier"
        verbose_name_plural = "Articles du panier"
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity


class UserProfile(models.Model):
    """Profil utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")
    city = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self):
        return f"Profil de {self.user.username}"


class Wishlist(models.Model):
    """Favoris"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, blank=True, verbose_name="Produits")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Liste de favoris"
        verbose_name_plural = "Listes de favoris"

    def __str__(self):
        return f"Favoris de {self.user.username}"


class Review(models.Model):
    """Avis produits"""
    RATING_CHOICES = [(i, f"{i} étoile{'s' if i > 1 else ''}") for i in range(1, 6)]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Note")
    title = models.CharField(max_length=200, verbose_name="Titre")
    comment = models.TextField(verbose_name="Commentaire")
    is_approved = models.BooleanField(default=True, verbose_name="Approuvé")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"


# ------------------------
# BLOG
# ------------------------

class BlogCategory(models.Model):
    """Catégorie de blog"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    color = models.CharField(max_length=7, default="#007bff", verbose_name="Couleur")

    class Meta:
        verbose_name = "Catégorie de blog"
        verbose_name_plural = "Catégories de blog"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """Article de blog"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    excerpt = models.TextField(max_length=300, verbose_name="Extrait")
    content = RichTextField(verbose_name="Contenu")
    image = models.ImageField(upload_to='blog/', verbose_name="Image")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0, verbose_name="Vues")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


# ------------------------
# AUTRES
# ------------------------

class Newsletter(models.Model):
    """Abonné newsletter"""
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=100, blank=True, verbose_name="Nom")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class FAQ(models.Model):
    """Questions fréquentes"""
    question = models.CharField(max_length=300, verbose_name="Question")
    answer = RichTextField(verbose_name="Réponse")
    category = models.CharField(max_length=100, blank=True, verbose_name="Catégorie")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ['order', 'question']

    def __str__(self):
        return self.question


class Contact(models.Model):
    """Message de contact"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"




class SiteInfo(models.Model):
    site_name = models.CharField(max_length=255, default="NaturalBio")
    logo = models.ImageField(upload_to="site/logo/", null=True, blank=True)
    favicon = models.ImageField(upload_to="site/favicon/", null=True, blank=True)

    # Couleurs Tailwind CSS
    primary_color = models.CharField(max_length=7, default="#2E7D32")
    accent_color = models.CharField(max_length=7, default="#A5D6A7")
    neutral_light = models.CharField(max_length=7, default="#F1F5F9")
    neutral_dark = models.CharField(max_length=7, default="#0F172A")
    success_color = models.CharField(max_length=7, default="#16A34A")
    warning_color = models.CharField(max_length=7, default="#F59E0B")
    danger_color = models.CharField(max_length=7, default="#DC2626")

    # Contact
    email_primary = models.EmailField(default="contact@naturalbio.com")
    phone_primary = models.CharField(max_length=50, default="+229 123 456 78")
    phone_secondary = models.CharField(max_length=50, blank=True, null=True)

    # Bannières et images
    payment_banner = models.ImageField(upload_to="site/banners/", null=True, blank=True)
    promo_banner = models.ImageField(upload_to="site/banners/", null=True, blank=True)

    # Texte promotionnel
    promo_text = models.CharField(max_length=255, blank=True, null=True, help_text="Texte affiché dans la barre promo")

    # Footer
    footer_text = models.TextField(default="© 2025 NaturalBio. Tous droits réservés.")

    class Meta:
        verbose_name = "Site Information"
        verbose_name_plural = "Site Information"

    def __str__(self):
        return self.site_name
