from django.contrib import admin
from .models import Spitch, Report


@admin.register(Spitch)
class SpitchAdmin(admin.ModelAdmin):
    list_display = ('user', 'ask', 'active', 'created')\


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('spitch', 'user', 'created')


