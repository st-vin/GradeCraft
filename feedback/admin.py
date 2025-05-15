from django.contrib import admin
from .models import FeedbackEntry

@admin.register(FeedbackEntry)
class FeedbackEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'get_summary_preview')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'input_summary', 'response')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Feedback Content', {
            'fields': ('input_summary', 'response')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_summary_preview(self, obj):
        """Return a shortened version of the input summary for the list view"""
        return obj.input_summary[:100] + '...' if len(obj.input_summary) > 100 else obj.input_summary
    get_summary_preview.short_description = 'Input Summary'
