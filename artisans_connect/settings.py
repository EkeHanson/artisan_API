# from datetime import timedelta
# from pathlib import Path
# import os
# import dj_database_url
# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-)kz2a!=-v&5c022cmljat9o9r5h2x#xtucrx*a)qfhi8wy+6$_'

# ESCROW_SANDBOX_SECRET_KEY = '4103_XM0g1jjqtwRv9X1NmTmWGfEPzTqv3OYAM7PBXghhSLopoZrNUAHSD8J7piIh2bfY'
# ESCROW_Email = 'ekehanson@gmail.com'
# # 4103_XM0g1jjqtwRv9X1NmTmWGfEPzTqv3OYAM7PBXghhSLopoZrNUAHSD8J7piIh2bfY

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = ['artisan-api-e2ih.onrender.com', 'localhost', '127.0.0.1']

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',

#     'rest_framework',
#     'rest_framework.authtoken',
#     'corsheaders',

#     'users',
#     'profiles',
#     'jobs',
#     'messaging',
#     'payments',
#     'chat',
#     # 'tradeReviews',
#     'artisanReview',
#     'quotes',
# ]


# # Ensure CORS middleware is at the top of the middleware list
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',  # Must be at the top
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'artisans_connect.urls'


# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]


# WSGI_APPLICATION = 'artisans_connect.wsgi.application'


# AUTH_USER_MODEL = 'users.CustomUser'



# # Add 'simservicehub.com' to the allowed origins
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "https://simservicehub.com",
#     "https://www.simservicehub.com",
#     "https://artisan-nu.vercel.app",
# ]

# # Allow credentials (if needed)
# CORS_ALLOW_CREDENTIALS = True



# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 10,

#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',  # Use JWTAuthentication
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
# }


# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.sqlite3',
# #         'NAME': BASE_DIR / 'db.sqlite3',
# #     }
# # }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'new_artisan_db_ras0',
#         'USER': 'new_artisan_db_ras0_user',
#         'PASSWORD': '5QlI0QVQ6ZKmj5PNTvz7XxIsNY9WOk7D',
#         'HOST': 'dpg-cudunstsvqrc73d251bg-a.oregon-postgres.render.com',
#         'PORT': '5432',  # Default PostgreSQL port
#     }
# }



# # Password validation
# # https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators


# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # Internationalization
# # https://docs.djangoproject.com/en/5.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/5.1/howto/static-files/

# STATIC_URL = 'static/'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# # Default primary key field type
# # https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# # enquiry@myhorizoncare.co.uk, e.o@myhorizoncare.co.uk
# # enquiry@myhorizoncare.co.uk, e.o@myhorizoncare.co.uk
# # ebiodumah@yahoo.com       ebiodumah@yahoo.com


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'mail.privateemail.com'
# EMAIL_PORT = 465
# EMAIL_USE_SSL = True
# EMAIL_HOST_USER = 'support@simservicehub.com'  # Your Hostinger email address
# EMAIL_HOST_PASSWORD = 'qwertyqwerty'  # Your Hostinger email password
# DEFAULT_FROM_EMAIL = 'support@simservicehub.com'  # Default sender email


# TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
# TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
# TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')


# # TWILIO_ACCOUNT_SID = 'SKde171cdf412a3ac995ee5add5b35fc10'  # Your Twilio Account SID
# # TWILIO_AUTH_TOKEN = 'DukdZ3OOflJhKJVcrCfkeb9Ab1nMv5Sl'
# # TWILIO_PHONE_NUMBER = '+15074426880'


# # TWILIO_ACCOUNT_SID = 'AC500ccdccd6ebc368dc82d8e36731e000'  # Your Twilio Account SID
# # TWILIO_AUTH_TOKEN = 'ba57440dbf551131d0eb006dd9fdedc2'
# # TWILIO_PHONE_NUMBER = '+15074426880'



from datetime import timedelta
from pathlib import Path
import os
import dj_database_url

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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_artisan_db_sc00',
        'USER': 'test_artisan_db_sc00_user',
        'PASSWORD': 'uX56iMstsVwV8lwu1wi6KmnHo6f3KIR3',
        'HOST': 'dpg-cuqtnftds78s7382mchg-a.oregon-postgres.render.com',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,  # Keeps connections open for performance
    }
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
#         'NAME': 'new_artisan_db_g9xw',
#         'USER': 'new_artisan_db_g9xw_user',
#         'PASSWORD': 'F1M5RUJyHGqyn0p2s70TZznXbvW4QldO',
#         'HOST': 'dpg-cumvu6ij1k6c73b4op4g-a.oregon-postgres.render.com',
#         'PORT': '5432',
#         'CONN_MAX_AGE': 600,  # Keeps connections open for better performance
#         'OPTIONS': {
#             'sslmode': 'require',  # Enforces SSL for secure connections
#         },
#     }
# }



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
EMAIL_HOST_PASSWORD = 'Michael@2024'
DEFAULT_FROM_EMAIL = 'support@simservicehub.com'

# CORS Configuration




