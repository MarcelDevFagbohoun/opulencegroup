from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!@=y@+#co!_$4f&-vnm0x1_biv67^c!awlso$)*y^-54-&q)ce'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','192.168.1.107']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'ckeditor',
    'ckeditor_uploader',
    'widget_tweaks',

]

# ------------------------
# Jazzmin settings
# ------------------------
JAZZMIN_SETTINGS = {
    "site_title": "Natural Bio Admin",
    "site_header": "Natural Bio Dashboard",
    "site_brand": "NaturalBio",
    "welcome_sign": "Bienvenue dans le Dashboard NaturalBio",
    "copyright": "NaturalBio © 2025",
    "show_sidebar": True,
    "navigation_expanded": True,
    "show_ui_builder": True,
    "topmenu_links": [
        {"name": "Site", "url": "/admin/core/siteinfo/", "permissions": ["core.view_siteinfo"]},
        {"name": "Shop", "app": "core"},
        {"name": "Blog", "app": "core"},
        {"name": "Users", "app": "auth"},
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "core.category": "fas fa-list-alt",
        "core.product": "fas fa-seedling",
        "core.order": "fas fa-shopping-cart",
        "core.orderitem": "fas fa-box",
        "core.cart": "fas fa-shopping-basket",
        "core.cartitem": "fas fa-box-open",
        "core.userprofile": "fas fa-id-card",
        "core.wishlist": "fas fa-heart",
        "core.review": "fas fa-star",
        "core.blogcategory": "fas fa-tags",
        "core.blogpost": "fas fa-newspaper",
        "core.newsletter": "fas fa-envelope-open",
        "core.faq": "fas fa-question-circle",
        "core.contact": "fas fa-envelope",
        "core.siteinfo": "fas fa-cog",
    },
    "related_modal_active": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "simple",        # simple et clair
    "dark_mode_theme": None,  # désactivé
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_color": "green",
    "accent": "green",
    "navbar": "white",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "footer_fixed": False,
    "body_rounded": True,
    "modals": "rounded",
    "buttons": "rounded",
}


CKEDITOR_UPLOAD_PATH = "uploads/"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'herbal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.services_pro',
                'core.context_processors.site_info',

            ],
        },
    },
]

WSGI_APPLICATION = 'herbal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Configuration de l'authentification
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Configuration des sessions
SESSION_COOKIE_AGE = 1209600  # 2 semaines
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True