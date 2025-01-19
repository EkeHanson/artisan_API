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
    'tradeReviews',
    'artisanReview',
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
CORS_ALLOW_ALL_ORIGINS = True

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


# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 10,

#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',  # Use TokenAuthentication
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
# }


# Email configuration

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  # Your SMTP server address
# EMAIL_PORT = 587  # Your SMTP server port (587 is the default for SMTP with TLS)
# EMAIL_USE_TLS = True  # Whether to use TLS (True by default)
# EMAIL_HOST_USER = 'ekenehanson@gmail.com'  # Your email address
# EMAIL_HOST_PASSWORD = 'pduw cpmw dgoq adrp'  # Your email password or app-specific password if using Gmail, etc.
# DEFAULT_FROM_EMAIL = 'ekenehanson@gmail.com'  # The default email address to use for sending emails


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'artisan_db_xtgx',
        'USER': 'artisan_db_xtgx_user',
        'PASSWORD': '0HbucQWFv2Vxb79rpEGXxUtiAVzzypNK',
        'HOST': 'dpg-cu652edsvqrc738ffn0g-a.oregon-postgres.render.com',
        'PORT': '5432',  # Default PostgreSQL port
    }
}





# DATABASES = {
#     'default': dj_database_url.parse(
#         'postgresql://artisan_db_xtgx_user:0HbucQWFv2Vxb79rpEGXxUtiAVzzypNK@dpg-cu652edsvqrc738ffn0g-a.oregon-postgres.render.com/artisan_db_xtgx',
#         conn_max_age=600,
#         ssl_require=True
#     )
# }



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


# Email settings for Hostinger
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 465  # SSL port
EMAIL_USE_SSL = True  # Use SSL for secure connection
EMAIL_HOST_USER = 'ekenehanson@sterlingspecialisthospitals.com'  # Your Hostinger email address
EMAIL_HOST_PASSWORD = '123@Qwertyqwerty@123'  # Your Hostinger email password
DEFAULT_FROM_EMAIL = 'ekenehanson@sterlingspecialisthospitals.com'  # Default sender email

DEFAULT_account_sid = 'AC500ccdccd6ebc368dc82d8e36731e000'  # Your Twilio Account SID
DEFAULT_auth_token = 'cc78f85b4552f9c448fcfbac0226b72c'    # Your Twilio Auth Token