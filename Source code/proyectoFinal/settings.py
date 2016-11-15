#encoding:utf-8
"""
Django settings for proyectoFinal project....

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AUTH_PROFILE_MODULE = 'users.UserProfile'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y!yaw=ug2_+t_p#50jzr%&qg71w4#@^ghjg^k$)(w+y_jsm(!%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

)

#TEMPLATE_CONTEXT_PROCESSORS = ()
#...

# Application definition

INSTALLED_APPS = (

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'proyectoFinal.telephones',
    'proyectoFinal.citys',
    'proyectoFinal.users',
    'proyectoFinal.complexes',
    'proyectoFinal.courts',
    'proyectoFinal.teams',
    'proyectoFinal.reservations',
    'proyectoFinal.matches',
    'proyectoFinal.tournaments',
    'proyectoFinal.fixtures',
    'proyectoFinal.playersinfo',
    'proyectoFinal.contacts',
    'proyectoFinal.publicities',
)

ROOT_URLCONF = 'proyectoFinal.urls'

WSGI_APPLICATION = 'proyectoFinal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': 'db_tesis'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATE_DIRS = [ os.path.join(os.path.dirname(__file__), 'templates')]

STATICFILES_DIRS = [ os.path.join(os.path.dirname(__file__), 'static')]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'service.minutogol@gmail.com'
EMAIL_HOST_PASSWORD = '36123477'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
