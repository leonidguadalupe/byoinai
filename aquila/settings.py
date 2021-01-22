import environ
import os

from celery.schedules import crontab
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environments taken from docker and some are from the default setting file
env = environ.Env(
    SECRET_KEY=(str, 'n+!i)4l9eok5bn=n80)l&ku8r00l^*(w8+kxkj0bwe^t7re93!'),
    DEBUG=(bool, True),
    ENVIRONMENT=(str, 'DEVELOPMENT'),
    ALLOWED_HOSTS=(list, []),
    LAKE_DB_NAME=(str, ""),
    LAKE_DB_USER=(str, ""),
    LAKE_DB_PASSWORD=(str, ""),
    LAKE_DB_HOST=(str, ""),
    LAKE_DB_PORT=(int, None),
    MART_DB_NAME=(str, ""),
    MART_DB_USER=(str, ""),
    MART_DB_PASSWORD=(str, ""),
    MART_DB_HOST=(str, ""),
    MART_DB_PORT=(int, None),
    LAKE_MSSQL_DB_NAME=(str, ""),
    LAKE_MSSQL_DB_USER=(str, ""),
    LAKE_MSSQL_DB_PASSWORD=(str, ""),
    LAKE_MSSQL_DB_HOST=(str, "")
)

# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')
DEVELOPMENT = 'DEVELOPMENT'
STAGING = 'STAGING'
PRODUCTION = 'PRODUCTION'
ENVIRONMENT = env('ENVIRONMENT')

LAKE_DB_NAME = env('LAKE_DB_NAME')
LAKE_DB_USER = env('LAKE_DB_USER')
LAKE_DB_PASSWORD = env('LAKE_DB_PASSWORD')
LAKE_DB_HOST = env('LAKE_DB_HOST')
LAKE_DB_PORT = env('LAKE_DB_PORT')
MART_DB_NAME = env('MART_DB_NAME')
MART_DB_USER = env('MART_DB_USER')
MART_DB_PASSWORD = env('MART_DB_PASSWORD')
MART_DB_HOST = env('MART_DB_HOST')
MART_DB_PORT = env('MART_DB_PORT')
LAKE_MSSQL_DB_NAME = env('LAKE_MSSQL_DB_NAME')
LAKE_MSSQL_DB_USER = env('LAKE_MSSQL_DB_USER')
LAKE_MSSQL_DB_PASSWORD = env('LAKE_MSSQL_DB_PASSWORD')
LAKE_MSSQL_DB_HOST = env('LAKE_MSSQL_DB_HOST')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aquila.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'aquila.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('MART_DB_NAME'),
        'USER': env('MART_DB_USER'),
        'PASSWORD': env('MART_DB_PASSWORD'),
        'HOST': env('MART_DB_HOST'),
        'PORT': env('MART_DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# celery settings

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_IMPORTS = ['jobs.tasks']

CELERY_BEAT_SCHEDULE = {
    'sync_external_db': {
        'task': 'jobs.tasks.sync_external_db',
        # Syncing of data runs every 2 minutes
        'schedule': crontab(minute="*/2")
    }
}