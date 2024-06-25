import phonenumbers
from django.core.exceptions import ValidationError
from phonenumber_field.phonenumber import to_python


def validate_iranian_phone_number(phone_number):
    phone_number = to_python(phone_number, 'IR')
    if (not phone_number.is_valid()
            or phone_number.country_code != 98
            or len(str(phone_number.national_number)) != 10
            or not str(phone_number.national_number).startswith('9')):
        raise ValidationError("Please enter a valid Iranian phone number.")


def validate_phone_number(phone_number, pk=None):
    from accounts.models import User
    validate_iranian_phone_number(phone_number)
    user = User.objects.filter(phone_number=phone_number)
    if pk:
        user = user.exclude(pk=pk)
    if user.exists():
        raise ValidationError('This phone number already exists')


def validate_email(email, pk=None):
    from accounts.models import User
    if email:
        user = User.objects.filter(email=email)
        if pk:
            user = user.exclude(pk=pk)
        if user.exists():
            raise ValidationError('This email already exists')
