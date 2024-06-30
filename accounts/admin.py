# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# local
from .models import OtpCode, User
from .forms import UserChangeForm, UserCreationForm


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_time')
    readonly_fields = ('created_time',)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('my_phone_number', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'last_login')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')
    ordering = ('first_name', 'last_name',)
    readonly_fields = ('last_login',)

    fieldsets = (
        ('Main', {'fields': ('email', 'phone_number', 'first_name', 'last_name', 'birthday', 'password')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",),
                'fields': ('phone_number', 'email', 'first_name', 'last_name', 'password1', 'password2')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form

    def my_phone_number(self, obj):
        return str(obj.phone_number).replace(' ', '')

    my_phone_number.allow_tags = True
    my_phone_number.short_description = _('شماره تلفن')
