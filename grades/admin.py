from django.contrib import admin
from .models import Grade, Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'unit', 'grade', 'semester', 'year', 'date_recorded')
    list_filter = ('grade', 'semester', 'year', 'date_recorded')
    search_fields = ('user__username', 'user__email', 'unit__name')
    ordering = ('-date_recorded',)
    readonly_fields = ('date_recorded',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Grade Information', {
            'fields': ('unit', 'grade', 'semester', 'year')
        }),
        ('Metadata', {
            'fields': ('date_recorded',),
            'classes': ('collapse',)
        }),
    )
