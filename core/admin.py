from django.contrib import admin
from .models import HeroSlide, Category, Product, SiteInfo,Service,ProductImage

# -----------------------
# HERO SLIDES ADMIN
# -----------------------
@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle_short', 'order', 'is_active', 'preview_image')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    ordering = ('order',)
    readonly_fields = ('preview_image',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'image', 'preview_image')
        }),
        ('Boutons', {
            'fields': (('button1_text', 'button1_url'), ('button2_text', 'button2_url'))
        }),
        ('Options', {
            'fields': ('order', 'is_active')
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="width: 300px; height:auto; border-radius: 10px;" />'
        return "-"
    preview_image.allow_tags = True
    preview_image.short_description = "Aperçu"

    def subtitle_short(self, obj):
        return obj.subtitle[:50] + ("..." if len(obj.subtitle) > 50 else "")
    subtitle_short.short_description = "Sous-titre"

# -----------------------
# SITE INFO ADMIN
# -----------------------
@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email_primary', 'phone_primary')
    readonly_fields = ('logo_preview', 'favicon_preview')

    fieldsets = (
        ('Informations Générales', {
            'fields': ('site_name', 'logo', 'logo_preview', 'favicon', 'favicon_preview')
        }),
        ('Couleurs', {
            'fields': ('primary_color', 'accent_color', 'neutral_light', 'neutral_dark', 'success_color', 'warning_color', 'danger_color')
        }),
        ('Contact', {
            'fields': ('email_primary', 'phone_primary', 'phone_secondary')
        }),
        ('Bannières', {
            'fields': ('payment_banner', 'promo_banner', 'promo_text')
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" style="height:50px;"/>'
        return "-"
    logo_preview.allow_tags = True
    logo_preview.short_description = "Logo"

    def favicon_preview(self, obj):
        if obj.favicon:
            return f'<img src="{obj.favicon.url}" style="height:30px;"/>'
        return "-"
    favicon_preview.allow_tags = True
    favicon_preview.short_description = "Favicon"

# -----------------------
# AUTRES MODELES (EXEMPLE)
# -----------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    prepopulated_fields = {"slug": ("name",)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # nombre de champs supplémentaires par défaut
    max_num = 5  # maximum d'images supplémentaires
    readonly_fields = ()
    fields = ('image', 'alt_text', 'order')
    show_change_link = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]  # ajoute les images supplémentaires ici


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description')