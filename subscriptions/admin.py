# Django
from django.contrib import admin

# local
from .models import Package, Subscription


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'title_en', 'is_active', 'price', 'duration']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'package', 'start_time', 'expire_time']
