# Django settings for qatrack project.
import django.conf.global_settings as DEFAULT_SETTINGS
import os
import sys

import matplotlib
matplotlib.use("Agg")

ALLOWED_HOSTS = ['*']

# -----------------------------------------------------------------------------
DEBUG = os.getenv('DEBUG', 'NO').lower() in ('on', 'true', 'y', 'yes')

# Who to email when server errors occur
ADMINS = (
    ('Admin Name', 'YOUR_EMAIL_ADDRESS_GOES_HERE'),
)
MANAGERS = ADMINS
SEND_BROKEN_LINK_EMAILS = True

# -----------------------------------------------------------------------------
# misc settings
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

VERSION = "0.3.0"
BUG_REPORT_URL = "https://bitbucket.org/tohccmedphys/qatrackplus/issues/new"
FEATURE_REQUEST_URL = BUG_REPORT_URL

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'qatrack.wsgi.application'

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['SECRET_KEY']
ROOT_URLCONF = 'qatrack.urls'

SITE_ID = 1
SITE_NAME = "QATrack+"

# -----------------------------------------------------------------------------
# Database settings

# if you wish to override the database settings below (e.g. for deployment),
# please do so here or in a local_settings.py file
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_SERVICE'],
        'PORT': os.environ['DB_PORT']
    }
}

# ----------------------------------------------------------------------------
# Default local settings

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Toronto'

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

FORMAT_MODULE_PATH = "qatrack.formats"

INPUT_DATE_FORMATS = (
    "%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M",
    "%d-%m-%y %H:%M", "%d/%m/%y %H:%M",
)
SIMPLE_DATE_FORMAT = "%d-%m-%Y"
DATETIME_HELP = "Format DD-MM-YY hh:mm (hh:mm is 24h time e.g. 31-05-12 14:30)"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

CONSTANT_PRECISION = 8

# This is the warning message given to the user when a test result is out of tolerance
# Override this setting in local_settings.py to a locally relevant warning message
DEFAULT_WARNING_MESSAGE = "Do not treat"

# ----------------------------------------------------------------------------
# static media settings

#  Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
TMP_UPLOAD_PATH = os.path.join("uploads", "tmp")
UPLOAD_ROOT = os.path.join(MEDIA_ROOT, "uploads")
TMP_UPLOAD_ROOT = os.path.join(UPLOAD_ROOT, "tmp")
for d in (MEDIA_ROOT, UPLOAD_ROOT, TMP_UPLOAD_ROOT):
    if not os.path.isdir(d):
        os.mkdir(d)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'
UPLOADS_URL = MEDIA_URL + 'uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

#  Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "admin_media"),
    # os.path.join(PROJECT_ROOT, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# add a site specific css file if one doesn't already exist
SITE_SPECIFIC_CSS_PATH = os.path.join(PROJECT_ROOT, "qatrack_core", "static", "qatrack_core", "css", "site.css")
if not os.path.isfile(SITE_SPECIFIC_CSS_PATH):
    with open(SITE_SPECIFIC_CSS_PATH, 'w') as f:
        f.write("/* You can place any site specific css in this file*/\n")


# ------------------------------------------------------------------------------
# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'qatrack.middleware.login_required.LoginRequiredMiddleware',
    'qatrack.middleware.maintain_filters.FilterPersistMiddleware',
)

# for django-debug-toolbar
INTERNAL_IPS = ('127.0.0.1',)


# login required middleware settings
LOGIN_EXEMPT_URLS = [r"^accounts/", ]
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/qa/unit/'
LOGIN_URL = "/accounts/login/"


# ------------------------------------------------------------------------------
# Template settings

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
            'genericdropdown/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                'qatrack.context_processors.site',
            ],
        },
    },
]

# ------------------------------------------------------------------------------
# Fixtures
# you can add more default fixture locations here
FIXTURE_DIRS = (
    'fixtures/defaults/qa',
    'fixtures/defaults/units',
)

# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'formtools',
    'tastypie',
    'listable',
    'genericdropdown',
    'crispy_forms',

    'qatrack.cache',
    'qatrack.accounts',
    'qatrack.units',
    'qatrack.qa',
    'qatrack.qatrack_core',

    'qatrack.notifications',
    'qatrack.contacts',
    'qatrack.attachments',

    'admin_views',
]
# -----------------------------------------------------------------------------
# Cache settings

CACHE_UNREVIEWED_COUNT = 'unreviewed-count'
CACHE_QA_FREQUENCIES = 'qa-frequencies'
MAX_CACHE_TIMEOUT = 24 * 60 * 60  # 24hours

CACHE_LOCATION = os.path.join(PROJECT_ROOT, "cache", "cache_data")
if not os.path.isdir(CACHE_LOCATION):
    os.mkdir(CACHE_LOCATION)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': CACHE_LOCATION,
        'TIMEOUT': MAX_CACHE_TIMEOUT,
    }
}

# -----------------------------------------------------------------------------
# Session Settings
SESSION_COOKIE_AGE = 14 * 24 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

# -----------------------------------------------------------------------------
# Email and notification settings
EMAIL_NOTIFICATION_USER = None
EMAIL_NOTIFICATION_PWD = None
EMAIL_NOTIFICATION_TEMPLATE = "notification_email.txt"
EMAIL_NOTIFICATION_SENDER = "qatrack"
# use either a static subject or a customizable template
# EMAIL_NOTIFICATION_SUBJECT = "QATrack+ Test Status Notification"
EMAIL_NOTIFICATION_SUBJECT_TEMPLATE = "notification_email_subject.txt"

EMAIL_FAIL_SILENTLY = True
EMAIL_HOST = ""  # e.g. 'smtp.gmail.com'
EMAIL_HOST_USER = ''  # e.g. "randle.taylor@gmail.com"
EMAIL_HOST_PASSWORD = 'your_password_here'
EMAIL_USE_TLS = True
EMAIL_PORT = 587


# -----------------------------------------------------------------------------
# Account settings
# a list of group names to automatically add users to when they sign up
DEFAULT_GROUP_NAMES = []  # eg ["Therapists"]

# -----------------------------------------------------------------------------
# Authentication backend settings
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'qatrack.accounts.backends.ActiveDirectoryGroupMembershipSSLBackend',
    # 'qatrack.accounts.backends.WindowsIntegratedAuthenticationBackend',
)

# active directory settings (not required if only using ModelBackend
AD_DNS_NAME = ''  # e.g. ad.civic1.ottawahospital.on.ca

# If using non-SSL use these
AD_LDAP_PORT = 389
AD_LDAP_URL = 'ldap://%s:%s' % (AD_DNS_NAME, AD_LDAP_PORT)
AD_LDAP_USER = ''
AD_LDAP_PW = ''

AD_LU_ACCOUNT_NAME = "sAMAccountName"
AD_LU_MAIL = "mail"
AD_LU_SURNAME = "sn"
AD_LU_GIVEN_NAME = "givenName"
AD_LU_MEMBER_OF = "memberOf"

# If using SSL use these:
# AD_LDAP_PORT=636
# AD_LDAP_URL='ldaps://%s:%s' % (AD_DNS_NAME,AD_LDAP_PORT)

AD_SEARCH_DN = ""  # eg "dc=ottawahospital,dc=on,dc=ca"
AD_NT4_DOMAIN = ""  # Network domain that AD server is part of

AD_SEARCH_FIELDS = [AD_LU_MAIL, AD_LU_SURNAME, AD_LU_GIVEN_NAME, AD_LU_ACCOUNT_NAME, AD_LU_MEMBER_OF]
AD_MEMBERSHIP_REQ = []  # eg ["*TOHCC - All Staff | Tout le personnel  - CCLHO"]
# AD_CERT_FILE='/path/to/your/cert.txt'

AD_DEBUG_FILE = None
AD_DEBUG = False

CLEAN_USERNAME_STRING = ''

# ------------------------------------------------------------------------------
# Logging Settings
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {

        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'qatrack.console': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

FORCE_SCRIPT_NAME = None

# ------------------------------------------------------------------------------
# QA Settings
PAGINATE_DEFAULT = 50  # remember to change iDisplayLength in unittestcollection.js and testlistinstance.js if you change this

NHIST = 5  # number of historical test results to show when reviewing/performing qa

ICON_SETTINGS = {
    'SHOW_STATUS_ICONS_PERFORM': True,
    'SHOW_STATUS_ICONS_LISTING': True,
    'SHOW_STATUS_ICONS_REVIEW': True,
    'SHOW_STATUS_ICONS_HISTORY': False,
    'SHOW_REVIEW_ICONS': True,
    'SHOW_DUE_ICONS': True,
}


# Display ordering on the "Choose Unit" page. (Use "name" or "number")
ORDER_UNITS_BY = "number"

# Enable or disable the "Difference" column when reviewing test lists
REVIEW_DIFF_COL = False

# default display settings for test statuses
TEST_STATUS_DISPLAY = {
    'fail': "Fail",
    'not_done': "Not Done",
    'done': "Done",
    'ok': "OK",
    'tolerance': "Tolerance",
    'action': "Action",
    'no_tol': "No Tol Set",
}

# default short display settings for test statuses
TEST_STATUS_DISPLAY_SHORT = {
    'fail': "Fail",
    'not_done': "Not Done",
    'done': "Done",
    'ok': "OK",
    'tolerance': "TOL",
    'action': "ACT",
    'no_tol': "NO TOL",
}

# ------------------------------------------------------------------------------
# local_settings contains anything that should be overridden
# based on site specific requirements (e.g. deployment, development etc)
try:
    from .local_settings import *  # NOQA
except ImportError:
    pass

if FORCE_SCRIPT_NAME:
    # Fix URL for Admin Views if FORCE_SCRIPT_NAME_SET in local_settings
    ADMIN_VIEWS_URL_PREFIX = FORCE_SCRIPT_NAME + "/admin"


# ------------------------------------------------------------------------------
# Testing settings

SELENIUM_VIRTUAL_DISPLAY = False # Set to True to use headless browser for testing (requires xvfb)
SELENIUM_USE_CHROME = False # Set to True to use Chrome instead of FF (requires ChromeDriver)
SELENIUM_CHROME_PATH = '' # Set full path of Chromedriver binary if SELENIUM_USE_CHROME == True


if 'test' in sys.argv:

    from .test_settings import * # noqa
