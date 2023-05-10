"""
Django settings for miniHospital project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import cloudinary.api
import cloudinary.uploader
import cloudinary
from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'doctor',
    'lab',
    'multiselectfield',
    'leave',
    'patient',
    'ckeditor',
    'captcha',
    'import_export',
    'paypal.standard.ipn',
    'dashboard',
    'rest_framework',
    'crispy_forms'


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


RECAPTCHA_PUBLIC_KEY = '6LfBwbMiAAAAAAbXL0saBDXbcJcKmg673cqVGLiY'
RECAPTCHA_PRIVATE_KEY = '6LfBwbMiAAAAANmqFckuf67fw1kEnOXo3puytod3'

ROOT_URLCONF = 'miniHospital.urls'

PAYPAL_TEST = True

SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-orgin-allow-popups'

RAZORPAY_API_KEY = 'rzp_test_19au902WXB3fFT'
RAZORPAY_API_SECRET_KEY = 'oXzTgMla8l4NduIz8hIWkQLp'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'miniHospital.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {

#     'default': {

#         'ENGINE': 'django.db.backends.postgresql_psycopg2',

#         'NAME': 'projectHospital',

#         'USER': 'postgres',

#         'PASSWORD': 'root',

#         'HOST': 'localhost',

#         'PORT': '5433',

#     }

# }

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'projectHospital',

        'USER': 'sajosam@vmedicare',

        'PASSWORD': 'Admin@000',

        'HOST': 'vmedicare.postgres.database.azure.com',

        'PORT': '5432',

        'OPTIONS': {
            "sslmode": "require",
        },

    }

}


AUTH_USER_MODEL = 'accounts.Account'


STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'miniHospital/static/'),]

# STATIC_ROOT = BASE_DIR/'staticfiles'


cloudinary.config(
    cloud_name="mini-hospital",
    api_key="187234116793571",
    api_secret="g6WHXy2HuZImrg7e3Nz2fpZfqFY"
)

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = config('SERVER_EMAIL')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
# MAILGUN_ACCESS_KEY = config('MAILGUN_ACCESS_KEY')

ACCOUNT_SID = config('ACCOUNT_SID')
AUTH_TOKEN = config('AUTH_TOKEN')
MESSAGING_SERVICE_SID = config('MESSAGING_SERVICE_SID')
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER')
