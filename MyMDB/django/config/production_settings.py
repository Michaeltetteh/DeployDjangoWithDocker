from .common_settings import *

DEBUG = False

assert SECRET_KEY is not None,(
    'Please provide DJANGO_SECRET_KEY'
    'environment variable with a value'
)

ALLOWED_HOSTS += [
    os.getenv('DJANGO_ALLOWED_HOSTS'),
]

#Database production config
DATABASES['default'].update({
    'NAME'      : os.getenv('DJANGO_DB_NAME'),
    'USER'      : os.getenv('DJANGO_DB_USER'),
    'PASSWORD'  : os.getenv('DJANGO_DB_PASSWORD'),
    'HOST'      : os.getenv('DJANGO_DB_HOST'),
    'PORT'      : os.getenv('DJANGO_DB_PORT'),
})

#cache production config
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmen.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIMEOUT' : int(os.getenv('DJANGO_CACHE_TIMEOUT'),),
    }
}

#inherites from common
#file uploads production config
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.s3Boto3Storage'
# AWS_ACCESS_KEY_ID  = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_ID')
# AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_UPLOAD_S3_BUCKET')


