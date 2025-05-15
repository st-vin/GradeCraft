from django.contrib import admin
from .models import AnalysisResult

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'gpa', 'classification', 'num_units', 'failing_units', 'timestamp')
    list_filter = ('classification', 'timestamp')
    search_fields = ('user__username', 'user__email')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Academic Performance', {
            'fields': ('gpa', 'classification', 'num_units', 'failing_units')
        }),
        ('Metadata', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
