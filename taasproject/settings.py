"""
Django settings for taasproject project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7sben+tr76v+2r37h)!)eb20%f3@uf$24dr64iod=qkysxu4xs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
   
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'rest_framework_swagger',
    'taasapp',
    'rest_framework',
    'versatileimagefield',
    'rest_framework.authtoken',
    'corsheaders',
    'easyaudit',
    'rest_framework_api_key',
    #'audit_trail',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware'
    #'audit_trail.middleware.AuditMiddleware',
]

ROOT_URLCONF = 'taasproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates/',],
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

WSGI_APPLICATION = 'taasproject.wsgi.application'
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# import pymysql
# pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taasdb',
        'USER': 'postgres',
        'PASSWORD': 'GABU#briel1',
        'HOST': 'localhost',  # or the hostname where your MySQL server is running
        'PORT': '',    
    }
}

AUTH_USER_MODEL = 'taasapp.Users'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        #'rest_framework_api_key.authentication.DRFTokenAPIKeyAuthentication',
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    'DATE_INPUT_FORMATS': [("%d-%m-%Y"),],
   
    # Other settings...
      'DEFAULT_PARSER_CLASSES': (
          'rest_framework.parsers.FormParser',
          'rest_framework.parsers.MultiPartParser',
          'rest_framework.parsers.JSONParser',
   )
}

REST_FRAMEWORK_API_KEY = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'NAME': 'Api-Key',
    'KEY_HEADER': 'Api-Key',
    'KEY_QUERY_PARAM': 'api_key',
    'KEY_CACHE_SECONDS': 60,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'DOOCUMEE API',
    'DESCRIPTION': 'API documentation for our Doocumme',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
    'COMPONENT_SPLIT_REQUEST': True
    # OTHER SETTINGS
}

SWAGGER_SETTINGS = {            
              'JSON_EDITOR': True,       
        }
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "taasapp_studenttranscript",
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Replace with your preferred backend
EMAIL_HOST_USER = 'email-smtp.us-east-1.amazonaws.com'  # Replace with your email host
EMAIL_PORT = 465  # Replace with your email port
#EMAIL_USE_TLS = True  # Set to False if your email server doesn't use TLS
EMAIL_HOST_USER = 'AKIA6BG6XTKIE3AVL72U'  # Replace with your email username
EMAIL_HOST_PASSWORD = 'BGG+Wm+yPci0u47znTLDiC0SqBEuVCVbg/5dNgNiT3sM'  # Replace with your email password

CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]
CORS_ALLOW_HEADERS = [
    # other headers
    'Authorization-Key',
]
CORS_ORIGIN_ALLOW_ALL=True
# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:3000',
# )
# CORS_EXPOSE_HEADERS = [
#     "my-custom-header",
# ]
# CORS_ALLOW_HEADERS = [
#     "localhost:3000",
# ]

# CORS_ALLOWED_ORIGINS  = [
#     'http://127.0.0.1:3000'
# ]
# Inter

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

import os
MEDIA_URL = '/media/logo/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/logo')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
