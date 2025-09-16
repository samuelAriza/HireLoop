from django.contrib import admin
from .models import Service, Cart, CartItem, Wishlist, WishlistItem


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'freelancer', 'category', 'price', 'delivery_time', 'active', 'created_at']
    list_filter = ['category', 'active', 'created_at']
    search_fields = ['title', 'description', 'freelancer__user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('freelancer', 'title', 'description', 'category')
        }),
        ('Detalles del Servicio', {
            'fields': ('price', 'delivery_time', 'active')
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_items', 'total_price']
    inlines = [CartItemInline]


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0
    readonly_fields = ['added_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['id', 'created_at', 'updated_at', 'total_items']
    inlines = [WishlistItemInline]