# Django
from django.utils.translation import gettext_lazy as _

# local
from rest_framework import serializers
from .validators import validate_phone_number, validate_email
from .models import User, OtpCode

# third party
from rest_framework.serializers import ModelSerializer
from phonenumber_field.serializerfields import PhoneNumberField


class LoginSerializer(ModelSerializer):
    phone_number = PhoneNumberField(region='IR')

    class Meta:
        model = User
        fields = ('phone_number', 'password')


class RegisterSerializer(ModelSerializer):
    phone_number = PhoneNumberField(region='IR', validators=[validate_phone_number, ])
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'password', 'password2', 'first_name', 'last_name', 'birthday')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {"validators": [validate_email], },
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError(_("دو رمز عبور وارد شده مطابقت ندارد."))
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class VerifyCodeSerializer(ModelSerializer):
    phone_number = PhoneNumberField(region='IR', validators=[validate_phone_number, ])

    class Meta:
        model = OtpCode
        fields = ('code', 'phone_number')

    def create(self, validate_data):
        otp = OtpCode.objects.get(**validate_data)
        otp.confirmation = True
        otp.save(update_fields=['confirmation'])
        return otp


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'phone_number', 'email', 'birthday')
