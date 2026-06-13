from pathlib import Path
import os

# base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# secret key - in production this must be set as environment variable
# never share or commit this key
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-finddjango-secret-key-change-in-production')

# debug mode - set to False in production
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# only allow requests from our actual domain
ALLOWED_HOSTS = ['findjango.onrender.com', '127.0.0.1', 'localhost']


# apps installed in this project
INSTALLED_APPS = [
    # default django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my finance tracker app
    'tracker',
]


# middleware runs on every request and response
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # whitenoise for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',    # csrf protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'findjango.urls'


# template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # look for templates in root templates folder
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

WSGI_APPLICATION = 'findjango.wsgi.application'


# database - using sqlite3 for development
# for production should switch to postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# password validation rules
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# language and timezone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # india timezone
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# static files (css, js)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
# whitenoise compresses and serves static files efficiently
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# media files (user uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# login settings
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'  # redirect here after login

# store messages in session
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
