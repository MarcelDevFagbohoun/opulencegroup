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
    image = models.ImageField(upload_to='products/', verbose_name="Image principale")  # image principale
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
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

class ProductImage(models.Model):
    """Images supplémentaires pour un produit"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/additional/', verbose_name="Image")
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")  # pour trier les images

    class Meta:
        verbose_name = "Image produit"
        verbose_name_plural = "Images produit"
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - Image {self.pk}"


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



class HeroSlide(models.Model):
    title = models.CharField(max_length=200, help_text="Titre principal du slide")
    subtitle = models.TextField(blank=True, help_text="Sous-titre ou description")
    image = models.ImageField(upload_to='hero_slides/')
    button1_text = models.CharField(max_length=50, blank=True, help_text="Texte du bouton 1")
    button1_url = models.URLField(blank=True, help_text="URL du bouton 1")
    button2_text = models.CharField(max_length=50, blank=True, help_text="Texte du bouton 2")
    button2_url = models.URLField(blank=True, help_text="URL du bouton 2")
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title



class Service(models.Model):
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=100, help_text="Classe FontAwesome, ex: fas fa-hard-hat")
    description = models.TextField(help_text="Courte description du service")
    details = models.TextField(help_text="Liste des projets, séparés par des sauts de ligne")
    whatsapp_link = models.URLField(help_text="Lien pour commander via WhatsApp")
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

    def details_list(self):
        """Retourne les détails sous forme de liste pour le template"""
        return [line.strip() for line in self.details.splitlines() if line.strip()]
