from django.contrib import admin
from .models import MentorshipSession, MentorshipReview


@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'mentor', 'mentee', 'category', 'price', 'duration_hours', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'mentor__user__username', 'mentee__user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('mentor', 'mentee', 'title', 'description', 'category')
        }),
        ('Detalles de la Sesión', {
            'fields': ('price', 'duration_hours', 'status')
        }),
        ('Programación', {
            'fields': ('scheduled_datetime', 'meeting_link')
        }),
        ('Información Adicional', {
            'fields': ('notes',)
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'mentor__user', 'mentee__user'
        )


@admin.register(MentorshipReview)
class MentorshipReviewAdmin(admin.ModelAdmin):
    list_display = ['session', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['session__title', 'reviewer__user__username', 'comment']
    readonly_fields = ['id', 'created_at']
    
    fieldsets = (
        (None, {
            'fields': ('session', 'reviewer', 'rating', 'comment')
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'session', 'reviewer__user'
        )
