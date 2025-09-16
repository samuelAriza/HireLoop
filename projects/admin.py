from django.contrib import admin
from .models import Project, ProjectApplication


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'state', 'budget', 'deadline', 'created_at']
    list_filter = ['state', 'created_at']
    search_fields = ['title', 'description', 'client__user__username']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('client', 'title', 'description')
        }),
        ('Detalles del Proyecto', {
            'fields': ('budget', 'deadline', 'state')
        }),
        ('Metadatos', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectApplication)
class ProjectApplicationAdmin(admin.ModelAdmin):
    list_display = ['project', 'freelancer', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['project__title', 'freelancer__user__username']
    readonly_fields = ['id', 'created_at']
