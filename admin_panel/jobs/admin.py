from django.contrib import admin
from django import forms
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from .models import Job
from django.utils.html import format_html


class JobAdminForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = []
        widgets = {
            'remote': DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-primary"),
        }


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    form = JobAdminForm
    list_display = ('title', 'get_url', 'experience','remote',
                    'source', 'posted_at')
    ordering = ('-posted_at',)
    list_filter = ('experience', 'remote', 'source')
    search_fields = ('title', 'skills', 'description')

    def get_url(self, obj):
        return format_html(f"<a target='_blank' href='{obj.url}'>Link</a>")

    get_url.short_description = "URL"
