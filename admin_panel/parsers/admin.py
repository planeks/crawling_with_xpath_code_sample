from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from boolean_switch.admin import AdminBooleanMixin
from django.contrib import admin
from django import forms
from .models import Parser, ScheduledTimePoint


class ScheduledTimePointInline(admin.TabularInline):
    model = ScheduledTimePoint
    extra = 0


class ParserAdminForm(forms.ModelForm):
    class Meta:
        model = Parser
        exclude = []
        widgets = {
            'active': DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success"),
        }


@admin.register(Parser)
class ParserAdmin(AdminBooleanMixin, admin.ModelAdmin):
    form = ParserAdminForm
    list_display = ['name', 'active']
    inlines = [ScheduledTimePointInline, ]
