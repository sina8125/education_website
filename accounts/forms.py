import phonenumbers
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password

from .models import User
from .validators import validate_phone_number, validate_email, validate_iranian_phone_number


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    error_messages = {
        "password_mismatch": "The two password fields didn’t match."
    }

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'password1', 'password2')
        field_classes = {'phone_number': PhoneNumberField}
        widgets = {
            'phone_number': RegionalPhoneNumberWidget(region='IR'),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email)
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        validate_phone_number(phone_number)
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'birthday', 'email', 'last_login', 'password')
        field_classes = {'phone_number': PhoneNumberField}
        widgets = {
            'phone_number': RegionalPhoneNumberWidget(region='IR'),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        validate_phone_number(phone_number, self.instance.pk)
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email, self.instance.pk)
        return email


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(widget=forms.EmailInput, required=False)
    birthday = forms.DateField(required=False)
    phone_number = PhoneNumberField(label='Phone number', region='IR', required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)

    error_messages = {
        "password_mismatch": "The two password fields didn’t match."
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email)
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        validate_phone_number(phone_number)
        return phone_number

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        validate_password(password2)
        return password2


class VerifyPhoneNumberForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone_number = PhoneNumberField(region='IR', required=True, widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    # error_messages = {
    #     "invalid_login":
    #         "Please enter a correct %(phone_number) and password. Note that both "
    #         "fields may be case-sensitive."
    #     ,
    #     "inactive": "This accounts is inactive.",
    # }
    #
    # def __init__(self, request=None, *args, **kwargs):
    #     self.request = request
    #     self.user_cache = None
    #     super().__init__(*args, **kwargs)
    #
    # def clean(self):
    #     phone_number = self.cleaned_data.get("phone_number")
    #     password = self.cleaned_data.get("password")
    #     if phone_number and password:
    #         self.user_cache = authenticate(
    #             self.request, phone_number=phone_number, password=password
    #         )
    #         if self.user_cache is None:
    #             raise self.get_invalid_login_error()
    #         else:
    #             self.confirm_login_allowed(self.user_cache)
    #
    #     return self.cleaned_data
    #
    # def confirm_login_allowed(self, user):
    #     """
    #     Controls whether the given User may log in. This is a policy setting,
    #     independent of end-user authentication. This default behavior is to
    #     allow login by active users, and reject login by inactive users.
    #
    #     If the given user cannot log in, this method should raise a
    #     ``ValidationError``.
    #
    #     If the given user may log in, this method should return None.
    #     """
    #     if not user.is_active:
    #         raise ValidationError(
    #             self.error_messages["inactive"],
    #             code="inactive",
    #         )
    #
    # def get_user(self):
    #     return self.user_cache
    #
    # def get_invalid_login_error(self):
    #     return ValidationError(
    #         self.error_messages["invalid_login"],
    #         code="invalid_login",
    #     )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    error_messages = {
        "password_incorrect": "Your old password was entered incorrectly. Please enter it again.",
        "password_mismatch": "The two password fields didn’t match.",
        "duplicated_password": "old password same as new password"
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        old_password = self.cleaned_data.get("old_password")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        if password1 and password2 and password2 == old_password:
            raise ValidationError(
                self.error_messages["duplicated_password"],
                code="duplicated_password",
            )
        validate_password(password2)
        return password2

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password
