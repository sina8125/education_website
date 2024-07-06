# Django
from django.contrib import admin

# local
from .models import Package, Subscription

# third party
from modeltranslation.admin import TranslationAdmin


@admin.register(Package)
class PackageAdmin(TranslationAdmin):
    list_display = ['pk', 'title', 'is_active', 'price', 'duration']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'start_time', 'expire_time']
