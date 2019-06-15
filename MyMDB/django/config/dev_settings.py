from .common_settings import *

DEBUG = True
SECRET_KEY = 'hj*n587%84;5456][56]=!=%etfg4452ewg46e3e0*90dagrwyafelmbwxf@d#vpi^s00pxuc'

INTERNAL_IPS =('127.0.0.1','172.17.0.1')

INSTALLED_APPS += [
    'debug_toolbar',
]


DATABASES['default'].update({
    'NAME': 'mymdb',
    'USER': 'postgres',
    'PASSWORD': 'KMF)jmf2-92[2[5kvm-n6v9=o53:2PM6',
    'HOST': '127.0.0.1',
    'PORT':'5432',
})

#Cache configs
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIMEOUT' : 5,
    }
}


# MEDIA_ROOT = os.path.join(BASE_DIR,'../media_root')
