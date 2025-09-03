from django.contrib import admin
from .models import (
    Category, Product, Order, OrderItem, Cart, CartItem, SiteInfo, UserProfile,
    Wishlist, Review, BlogCategory, BlogPost, Newsletter, FAQ, Contact
)


# ------------------------
# E-COMMERCE
# ------------------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active", "is_featured", "created_at")
    list_filter = ("is_active", "is_featured", "category")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "total_amount", "created_at", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "delivery_name", "delivery_phone")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "updated_at", "delivered_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price", "total_price")
    search_fields = ("order__id", "product__name")


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "total_items", "total_price", "created_at", "updated_at")
    inlines = [CartItemInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "added_at")
    list_filter = ("added_at",)
    search_fields = ("product__name",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "city", "created_at")
    search_fields = ("user__username", "phone", "city")
    readonly_fields = ("created_at",)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    filter_horizontal = ("products",)  # interface sympa pour les ManyToMany


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "is_approved", "created_at")
    list_filter = ("rating", "is_approved", "created_at")
    search_fields = ("product__name", "user__username", "title", "comment")
    readonly_fields = ("created_at",)


# ------------------------
# BLOG
# ------------------------

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "color")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "views", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("views", "created_at", "updated_at")


# ------------------------
# AUTRES
# ------------------------

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "is_active", "subscribed_at")
    list_filter = ("is_active",)
    search_fields = ("email", "name")
    readonly_fields = ("subscribed_at",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "order", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("question", "answer")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)



@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email_primary', 'phone_primary')
    list_display_links = ('site_name',)
    readonly_fields = ('logo_preview', 'payment_banner_preview')
    fieldsets = (
        ('General Information', {
            'fields': ('site_name', 'favicon', 'logo', 'logo_preview', 'promo_text')
        }),
        ('Colors (Tailwind CSS)', {
            'fields': ('primary_color', 'accent_color', 'neutral_light', 'neutral_dark', 'success_color', 'warning_color', 'danger_color')
        }),
        ('Contact', {
            'fields': ('email_primary', 'phone_primary', 'phone_secondary')
        }),
        ('Banners & Images', {
            'fields': ('payment_banner', 'payment_banner_preview', 'promo_banner')
        }),
        ('Footer', {
            'fields': ('footer_text',)
        }),
    )

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" style="height: 100px;"/>'
        return "No logo uploaded"
    logo_preview.allow_tags = True
    logo_preview.short_description = "Logo Preview"

    def payment_banner_preview(self, obj):
        if obj.payment_banner:
            return f'<img src="{obj.payment_banner.url}" style="height: 50px;"/>'
        return "No payment banner uploaded"
    payment_banner_preview.allow_tags = True
    payment_banner_preview.short_description = "Payment Banner Preview"

    def has_add_permission(self, request):
        """Allow only one SiteInfo instance (single modal)."""
        return not SiteInfo.objects.exists()

