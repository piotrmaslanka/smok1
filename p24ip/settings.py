# Django settings for p24 project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'mysql'  
DATABASE_NAME = 'p24'      
DATABASE_USER = 'root'     
DATABASE_PASSWORD = ''
DATABASE_HOST = 'localhost'
DATABASE_PORT = ''
TIME_ZONE = 'Europe/Warsaw'
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

LANGUAGE_CODE = 'pl'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'xxx'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'djangomako.middleware.MakoMiddleware',
)

ROOT_URLCONF = 'p24ip.urls'

TEMPLATE_DIRS = (
    '/var/www/html/p24ip/templates',
)

INSTALLED_APPS = (
    'django.contrib.sessions',
    'p24ip.login',
    'p24ip.manage',
    'p24ip.device',
    'p24ip.arch',
    'p24ip.publica',
    'p24ip.dispatch',
)
