"""
Django settings for {{Shop}} project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os

from pathlib import Path
from dotenv import load_dotenv

# import accounts.forms
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY_SHOP')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = [      # # Этого раздела может не быть, добавьте его в указанном виде.
    'django.contrib.auth.backends.ModelBackend',  # реализующий аутентификацию по username;
    'allauth.account.auth_backends.AuthenticationBackend',]  # бэкенд аутентификации, предоставленный пакетом


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # added apps
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'django_apscheduler',
    # apps for allauth. три обязательных приложения для работы allauth и одно,
    # которое добавит поддержку входа с помощью Yandex
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # user apps:
    'accounts',
    'market',
]

SITE_ID = 1  # используется в случае, если данный проект управляет несколькими сайтами

LOGIN_REDIRECT_URL = '/products'
LOGOUT_REDIRECT_URL = '/products'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # mandatory for allauth
    'allauth.account.middleware.AccountMiddleware',
    # add for caching for full site
    # "django.middleware.cache.UpdateCacheMiddleware",
    # "django.middleware.common.CommonMiddleware",
    # "django.middleware.cache.FetchFromCacheMiddleware",
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {'client_id': os.getenv('GOOGLE_CLIENT_ID'),
                'secret': os.getenv('GOOGLE_SECRET')}
    }
}

ROOT_URLCONF = '{{Shop}}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # added apps for allauth
                'django.template.context_processors.request'  # контекстный процессор
            ],
        },
    },
]

WSGI_APPLICATION = '{{Shop}}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),  # Указываем, куда будем сохранять кэшируемые файлы!
        # Не забываем создать папку cache_files внутри папки с manage.py!
        # 'TIMEOUT': 30,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR/'static']

# Constance for allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True # для перехода на страницу входа
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

ACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSignupForm'}  # добавили применение касто-формы

SITE_URL = 'http://127.0.0.1:8000'
# Constance for mailinf from Yandex
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # django.core.mail.backends.console.EmailBackend
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('USER_NAME_YANDEX')
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWD_YANDEX")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = os.getenv('USER_NAME_YANDEX')

SERVER_EMAIL = os.getenv('USER_NAME_YANDEX')
MANAGERS = (
    ('Andrey', os.getenv('USER_NAME_YANDEX')),
    # ('Petr', 'petr@yandex.ru'),
)
ADMINS = (
    ('Andrey', os.getenv('USER_NAME_YANDEX')),
)

# APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'  № внутрениий формат даты
# APSCHEDULER_RUN_NOW_TIMEOUT = 25  # время работы функции для контроля памяти


CELERY_BROKER_URL = 'redis://localhost:6379'  # указывает на URL брокера сообщений (Redis).
# По умолчанию находится на порту 6379
CELERY_RESULT_BACKEND = 'redis://localhost:6379'  # указывает на хранилище результатов выполнения задач
CELERY_ACCEPT_CONTENT = ['application/json']  # допустимый формат данных
CELERY_TASK_SERIALIZER = 'json'  # метод сериализации задач
CELERY_RESULT_SERIALIZER = 'json'  # метод сериализации результатов