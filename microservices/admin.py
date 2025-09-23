from django.contrib import admin
from .models import Category, MicroService


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}  # autocompleta slug a partir del nombre
    list_display = ("name", "slug")


@admin.register(MicroService)
class MicroServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "freelancer", "category", "price", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("title", "description")
