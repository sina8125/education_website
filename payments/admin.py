# Django
from django.contrib import admin

# local
from payments.models import Payment

admin.site.register(Payment)
