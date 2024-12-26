from pathlib import Path
import os  # Add this import to use os.path.join()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-tp69gtna1!7y!+m9v^##n08dynb9&yh8+i@ibl!o&k0er^z(6d"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []  # Add allowed hosts for production when needed

# Application definition
INSTALLED_APPS = [
    'jazzmin',
   
    'admin_notifications',

    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blood_bank', 
]


# # # #jazzmin ka jalwa by Muhtasim

JAZZMIN_SETTINGS = {
    "site_title": "Blood Bank Admin",
    "site_header": "Blood Bank Management System",
    "site_brand": "Blood Bank",
    "welcome_sign": "Welcome to Blood Bank Admin Panel",
    "site_logo": "images/logo11.jpg",  # Add your logo here
    "copyright": "Blood Bank Admin",
    "search_model": "your_app_name.YourModel",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Support", "url": "https://support.example.com", "new_window": True},
        {"model": "auth.User"},
        {"app": "blood_bank"},
    ],
    "site_logo": "images/logo11.jpg",  # Your site logo
    "custom_links": {
        "global": [
            {
                "name": "View Site",          # Link text
                "url": "/",                  # URL path (relative to root domain)
                "icon": "fas fa-globe",      # Optional: FontAwesome icon
                "permissions": ["auth.view_user"],  # Optional: Restrict based on permissions
            }
        ]
    },
    "topmenu_links": [
        # Custom View Site link
        {"name": "View Site", "url": "/", "new_window": True},

        # Existing menu links
        {"model": "auth.User"},  # Example
        {"app": "blood_bank"},  # Link to your app
    ],
}


# JAZZMIN_UI_TWEAKS = {
#     "theme": "default",  # Options: 'default', 'dark', 'light'
#     # "dark_mode_theme": "darkly",
#     # "navbar": "navbar-dark bg-primary",
#     # "sidebar": "sidebar-dark-primary",
#     # "navbar": "navbar-light bg-light",
#     # "sidebar": "sidebar-light-primary"
# }

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "navbar": "navbar-dark bg-primary",
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# # # #new jazzmin settings updated by moinul

# # Jazzmin configuration for admin customization
# JAZZMIN_SETTINGS = {
#     # General settings for branding and site information
#     "site_title": "Blood Bank Admin",  # Title shown on the browser tab
#     "site_header": "Blood Bank",  # Header displayed on the admin interface
#     "site_brand": "Blood Bank MS",  # Branding name in the admin interface
#     "site_logo": "images/logo11.jpg",  # Path to the logo image
#     "welcome_sign": "Welcome to Blood Bank Management System",  # Welcome message
#     "copyright": "Blood Bank Management System © 2024",  # Footer copyright
#     "search_model": ["blood_bank.BloodInventory", "blood_bank.BloodGroup"],  # Models to search in the admin panel
#     "user_avatar": None,  # Placeholder for user profile pictures

#     # Top menu links for navigation
#     "topmenu_links": [
#         {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},  # Link to admin home
#         {"name": "Blood Bank", "url": "/blood-bank", "permissions": ["blood_bank.view_bloodinventory"]},  # Example link
#         {"app": "blood_bank"},  # Link to the blood_bank app
#     ],

#     # Model icons for a modern and intuitive UI
#     "icons": {
#         "auth": "fas fa-users-cog",
#         "auth.user": "fas fa-user",
#         "auth.group": "fas fa-users",
#         "blood_bank.bloodgroup": "fas fa-tint fa-lg",
#         "blood_bank.donor": "fas fa-user-plus fa-lg",
#         "blood_bank.recipient": "fas fa-procedures fa-lg",
#         "blood_bank.recipient2": "fas fa-user-injured fa-lg",
#         "blood_bank.profile": "fas fa-id-card fa-lg",
#         "blood_bank.bloodinventory": "fas fa-warehouse fa-lg",
#         "blood_bank.donorreg": "fas fa-user-plus fa-lg",
#     },

#     # Custom ordering of models in the admin sidebar
#     "order_with_respect_to": [
#         "blood_bank",  # Blood bank app first
#         "blood_bank.BloodInventory",
#         "blood_bank.BloodGroup",
#         "blood_bank.Donor",
#         "blood_bank.Recipient",
#         "blood_bank.Recipient2",
#         "blood_bank.Profile",
#         "blood_bank.DonorReg",
#         "auth",  # Auth app next
#     ],

#     # UI enhancements
#     "show_sidebar": True,  # Keep sidebar visible
#     "navigation_expanded": True,  # Sidebar expanded by default
#     "hide_apps": [],  # Apps to hide in the sidebar
#     "hide_models": [],  # Models to hide in the sidebar
#     "custom_css": "blood_bank/css/custom.css",  # Path to custom CSS for styling
#     "custom_js": "blood_bank/js/custom.js",  # Path to custom JavaScript for functionality
#     "show_ui_builder": True,  # Allow the UI builder for quick layout changes
#     "changeform_format": "horizontal_tabs",  # Tabbed view for model change forms
#     "related_modal_active": True,  # Enable modals for related models

#     # Custom links for actions
#     "custom_links": {
#         "blood_bank": [{
#             "name": "Generate Report",  # Link name
#             "url": "admin:blood_bank_report",  # Admin link for report generation
#             "icon": "fas fa-file-pdf",  # FontAwesome icon for the link
#         }],
#     },
# }

# # Jazzmin UI tweaks for additional styling and layout control
# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": False,  # Normal text size for the navbar
#     "footer_small_text": False,  # Normal text size for the footer
#     "body_small_text": False,  # Normal text size for the body
#     "brand_small_text": False,  # Normal text size for the brand
#     "brand_colour": "navbar-primary",  # Navbar color for branding
#     "accent": "accent-primary",  # Primary accent color
#     "navbar": "navbar-dark",  # Navbar theme (dark mode)
#     "no_navbar_border": False,  # Show border for the navbar
#     "navbar_fixed": True,  # Fix the navbar at the top
#     "layout_boxed": False,  # Disable boxed layout
#     "footer_fixed": False,  # Footer not fixed at the bottom
#     "sidebar_fixed": True,  # Sidebar fixed in place
#     "sidebar": "sidebar-dark-warning",  # Sidebar theme
#     "sidebar_nav_small_text": False,  # Normal text size for the sidebar
#     "sidebar_disable_expand": False,  # Allow sidebar to expand
#     "sidebar_nav_child_indent": True,  # Indent child menu items in the sidebar
#     "sidebar_nav_compact_style": False,  # Use default style for the sidebar
#     "sidebar_nav_legacy_style": False,  # Disable legacy style
#     "sidebar_nav_flat_style": False,  # Use hierarchical sidebar navigation
#     "theme": "slate",  # Set theme to "slate" for modern look
#     "dark_mode_theme": "darkly",  # Set dark mode theme to "darkly"
#     "button_classes": {  # Define custom button styles
#         "primary": "btn-outline-primary",
#         "secondary": "btn-outline-secondary",
#         "info": "btn-outline-info",
#         "warning": "btn-outline-warning",
#         "danger": "btn-outline-danger",
#         "success": "btn-outline-success"
#     },
#     "actions_sticky_top": True,  # Keep action buttons sticky at the top
# }

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blood_bank_project.urls"

# TEMPLATES setting
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'blood_bank/templates')],  # This line includes the path to templates
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

WSGI_APPLICATION = "blood_bank_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login URL setting
LOGIN_URL = '/login/'
#updated by me
# LOGOUT_REDIRECT_URL = 'admin/login/'

# Redirect to profile page after login
LOGIN_REDIRECT_URL = '/profile/'  # This will redirect the user to their profile page after login


AUTH_USER_MODEL = 'auth.User'  # Using Django's built-in User model

# Media configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]



