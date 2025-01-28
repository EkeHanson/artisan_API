from datetime import timedelta
from pathlib import Path
import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)kz2a!=-v&5c022cmljat9o9r5h2x#xtucrx*a)qfhi8wy+6$_'

ESCROW_SANDBOX_SECRET_KEY = '4103_XM0g1jjqtwRv9X1NmTmWGfEPzTqv3OYAM7PBXghhSLopoZrNUAHSD8J7piIh2bfY'
ESCROW_Email = 'ekehanson@gmail.com'
# 4103_XM0g1jjqtwRv9X1NmTmWGfEPzTqv3OYAM7PBXghhSLopoZrNUAHSD8J7piIh2bfY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['artisan-api-e2ih.onrender.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    'users',
    'profiles',
    'jobs',
    'messaging',
    'payments',
    'chat',
    # 'tradeReviews',
    'artisanReview',
    'quotes',
]


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be before CommonMiddleware
    'django.middleware.security.SecurityMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'artisans_connect.urls'


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


WSGI_APPLICATION = 'artisans_connect.wsgi.application'


AUTH_USER_MODEL = 'users.CustomUser'


MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

# Allow specific origins during development
CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",

#     # "http://simservicehub.com",

#     "https://artisan-nu.vercel.app"

#     "https://www.simservicehub.com"
# ]

# If you want to allow all origins during development (not recommended for production):


# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 10,  # 10 messages per page

#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
# }

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Use JWTAuthentication
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'cmvpdb_f4z3',
#         'USER': 'cmvpdb_f4z3_user',
#         'PASSWORD': '8TaIUwuTsy4QmAXk47QZR2jolq0bu5p2',
#         'HOST': 'dpg-cucddjqj1k6c73b95tig-a.oregon-postgres.render.com',
#         'PORT': '5432',  # Default PostgreSQL port
#     }
# }

DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://cmvpdb_f4z3_user:8TaIUwuTsy4QmAXk47QZR2jolq0bu5p2@dpg-cucddjqj1k6c73b95tig-a.oregon-postgres.render.com/cmvpdb_f4z3",
        conn_max_age=600,  # Set connection lifetime (in seconds) for persistent connections
        ssl_require=True   # Enforces SSL if required
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators


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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# enquiry@myhorizoncare.co.uk, e.o@myhorizoncare.co.uk
# enquiry@myhorizoncare.co.uk, e.o@myhorizoncare.co.uk
# ebiodumah@yahoo.com       ebiodumah@yahoo.com


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'support@simservicehub.com'  # Your Hostinger email address
EMAIL_HOST_PASSWORD = 'qwertyqwerty'  # Your Hostinger email password
DEFAULT_FROM_EMAIL = 'support@simservicehub.com'  # Default sender email


# TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
# TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
# TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')


TWILIO_ACCOUNT_SID = 'SKde171cdf412a3ac995ee5add5b35fc10'  # Your Twilio Account SID
TWILIO_AUTH_TOKEN = 'DukdZ3OOflJhKJVcrCfkeb9Ab1nMv5Sl'
TWILIO_PHONE_NUMBER = '+15074426880'


# TWILIO_ACCOUNT_SID = 'AC500ccdccd6ebc368dc82d8e36731e000'  # Your Twilio Account SID
# TWILIO_AUTH_TOKEN = 'ba57440dbf551131d0eb006dd9fdedc2'
# TWILIO_PHONE_NUMBER = '+15074426880'

