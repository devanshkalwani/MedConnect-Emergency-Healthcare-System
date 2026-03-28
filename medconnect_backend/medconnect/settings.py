from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# ===============================
# SECURITY
# ===============================
SECRET_KEY = 'django-insecure-medconnect-secret-key'

DEBUG = True

ALLOWED_HOSTS = ['*']


# ===============================
# APPLICATIONS
# ===============================
INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # THIRD PARTY
    'rest_framework',
    'corsheaders',

    # LOCAL
    'core',
]


# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # 🔥 MUST BE FIRST

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ===============================
# URL CONFIG
# ===============================
ROOT_URLCONF = 'medconnect.urls'


# ===============================
# TEMPLATES
# ===============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # you can add frontend templates later
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


# ===============================
# ASGI & WSGI
# ===============================
WSGI_APPLICATION = 'medconnect.wsgi.application'
ASGI_APPLICATION = 'medconnect.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


# ===============================
# DATABASE
# ===============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ===============================
# PASSWORD VALIDATION
# ===============================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]


# ===============================
# CUSTOM USER MODEL
# ===============================
AUTH_USER_MODEL = 'core.User'


# ===============================
# DRF CONFIG
# ===============================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
}


# ===============================
# CORS (🔥 VERY IMPORTANT)
# ===============================
CORS_ALLOW_ALL_ORIGINS = True


# ===============================
# INTERNATIONALIZATION
# ===============================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ===============================
# STATIC FILES
# ===============================
STATIC_URL = 'static/'


# ===============================
# DEFAULT PRIMARY KEY
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'