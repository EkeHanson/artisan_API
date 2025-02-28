from datetime import timedelta
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-)kz2a!=-v&5c022cmljat9o9r5h2x#xtucrx*a)qfhi8wy+6$_'

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
    # 'chat',
    'artisanReview',
    'quotes',
    'payouts',
    'subscription',
    'notification',
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
]

CORS_ALLOW_CREDENTIALS = True  # Allow credentials

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://simservicehub.com",
    "https://www.simservicehub.com",
    "https://artisan-nu.vercel.app",
]

CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'x-csrftoken',
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
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


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'test_artisan_db_wsnp',
#         'USER': 'test_artisan_db_wsnp_user',
#         'PASSWORD': 'yO6Akgaw8xYAjbuug9HXTugtY6ZeCLFq',
#         'HOST': 'dpg-cuu7ao1opnds739u13t0-a.oregon-postgres.render.com',
#         'PORT': '5432',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'simservice',
#         'USER': 'postgres',
#         'PASSWORD': 'pluralsight',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'simupwsv_simservicehub_db',
#         'USER': 'simupwsv_ekenehanson',
#         'PASSWORD': 'pluralsight',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'artisan_db_t3wt',
        'USER': 'artisan_db_t3wt_user',
        'PASSWORD': 'LRcOdNU9b5R55IpcUMZzvcqR4ofbjsT5',
        'HOST': 'dpg-cuv9nkdds78s73cipupg-a.oregon-postgres.render.com',
        'PORT': '5432',  # Default PostgreSQL port
        'OPTIONS': {
            'sslmode': 'require',  # Ensures secure connection
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # 10 messages per page

    'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework.authentication.TokenAuthentication',
    'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'support@simservicehub.com'
EMAIL_HOST_PASSWORD = 'Highwycombe02'
DEFAULT_FROM_EMAIL = 'support@simservicehub.com'

# CORS Configuration


# bulksmsnigeria_url = "https://www.bulksmsnigeria.com/api/v1/sms/create"
# BULK_SMS_api_token = "iChBOImG7e8CPbZbMvPV9yHBmFCfL0FfBtz4t5cJFkbZe97tt3Q0xxVteSCt",



