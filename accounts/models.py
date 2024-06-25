import os.path
import re
from inspect import isfunction
from os.path import join

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from accounts.validators import validate_iranian_phone_number


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, email, password, **extra_fields):
        """
        Create and save a user with the given phone_number, email, and password.
        """
        if not phone_number:
            raise ValueError("user must have phone number")
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, email, password, **extra_fields)

    def create_superuser(self, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, email, password, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):

    def set_avatar_path(self, filename):
        n = 1
        filename, file_extension = os.path.splitext(filename)
        if self.pk:
            previous_avatar = self.avatar.name
            if previous_avatar:
                number_of_avatar = re.match(r'^\d+_a(\d+)\.\w+$', previous_avatar).group(1)
                n = int(number_of_avatar) + 1
        return join('avatars', self.pk, f'{self.pk}_a{n}{file_extension}')

    phone_number = PhoneNumberField(region='IR', unique=True, null=False, blank=False,
                                    validators=[validate_iranian_phone_number])
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=True)
    nick_name = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(blank=True, upload_to=set_avatar_path)
    birthday = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_active_time = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        swappable = "AUTH_USER_MODEL"

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)

    @property
    def get_first_name(self):
        return self.first_name

    @property
    def get_last_name(self):
        return self.last_name

    def get_nickname(self):
        return self.nick_name or self.get_full_name()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self):
        return self.get_full_name() or self.email or str(self.phone_number)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()


class OtpCode(models.Model):
    phone_number = PhoneNumberField(region='IR', null=False, blank=False)
    code = models.PositiveSmallIntegerField()
    confirmation = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created_time}'

    class Meta:
        verbose_name = 'otpcode'
        verbose_name_plural = 'otpcodes'
