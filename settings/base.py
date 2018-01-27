import os
import raven
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """
    Get the environment variable or return exception
    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)




BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xxxxxxxxxxxxxx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = ['apps.core.auth.EmailOrUsernameModelBackend']


# Application definition

INSTALLED_APPS = [
    #Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Thirds apps
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'raven.contrib.django.raven_compat',
    #Own apps
    'apps.core.apps.CoreConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.relation.apps.RelationConfig',
    'apps.ask.apps.AskConfig',
    'apps.spitch.apps.SpitchConfig',
    'apps.feed.apps.FeedConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
        'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


AUTH_USER_MODEL = 'authentication.User'


REGISTER_CONFIRMATION = True




# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

#Django rest framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}



# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/





# AWS S3 SETTINGS

DEFAULT_FILE_STORAGE = 'apps.core.storages.MediaStorage'
STATICFILES_STORAGE = 'apps.core.storages.StaticStorage'

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'


AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'spitchdev-bucket-xxxxxxxxx'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)


AWS_META_DATA = {}



# Notification

DYNAMODB_TABLE = 'spitchdev-tableNotification-xxxxxxx'
DYNAMODB_REGION = 'eu-west-1'


# Sqs Worker

SQS_WORKER = 'https://sqs.eu-west-1.amazonaws.com/xxxxx/xxxxxx-sqsWorker-1AIORIAUBDA2I'


# ElasticSearch

NAME_ES_DOMAIN = 'xxxxx'



#Sentry

RAVEN_CONFIG = {
    'dsn': 'xxxxxxxx',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
}
