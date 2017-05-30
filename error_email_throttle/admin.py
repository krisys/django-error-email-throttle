from django.contrib import admin
from .models import ErrorReport
# Register your models here.


class ErrorReportAdmin(admin.ModelAdmin):
    list_display = [
        'filename', 'function', 'lineno', 'error_date',
        'latest_error', 'last_emailed', 'error_count', 'affected_urls'
    ]
    readonly_fields = [
        'filename', 'function', 'lineno', 'context_line', 'error_count',
        'urls', 'error_hash', 'last_emailed', 'error_date', 'latest_error',
        'stack_trace'
    ]


admin.site.register(ErrorReport, ErrorReportAdmin)
