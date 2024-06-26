"""
Django settings for education project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from django.utils.translation import gettext_lazy as _

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mptt',
    'phonenumber_field',
    'ckeditor',
    'ckeditor_uploader',
    'nested_inline',
    "azbankgateways",
    'rest_framework',

    'posts',
    'accounts',
    'subscriptions',
    'payments',
    'utils'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'education.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'posts.context_processors.category_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'education.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('fa-ir', _('فارسی')),
    ('en-us', _('انگلیسی')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',  # مسیر فایل‌های ترجمه
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root', 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login'

PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = "IR"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"

CKEDITOR_UPLOAD_PATH = "posts/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ','.join(
            [
                'html5video',
            ]),
    },
}

AZ_IRANIAN_BANK_GATEWAYS = {
    "GATEWAYS": {
        "IDPAY": {
            "MERCHANT_CODE": "6a7f99eb-7c20-4412-a972-6dfb7cd253a4",
            "METHOD": "POST",  # GET or POST
            "X_SANDBOX": 1,  # 0 disable, 1 active
        }
    },
    "IS_SAMPLE_FORM_ENABLE": True,  # اختیاری و پیش فرض غیر فعال است
    "DEFAULT": "IDPAY",
    "CURRENCY": "IRR",
    "TRACKING_CODE_QUERY_PARAM": "tc",
    "TRACKING_CODE_LENGTH": 16,
    "SETTING_VALUE_READER_CLASS": "azbankgateways.readers.DefaultReader",
    'CUSTOM_APP': 'payments',
    "IS_SAFE_GET_GATEWAY_PAYMENT": False
}

# import local settings
try:
    if os.environ.get('DJANGO_ENVIRONMENT'):
        from .local_settings import *
except Exception:
    pass
