from .base import *

SECRET_KEY = 'w#h+dk9^edk@0^o8qms%9wsa&hde3%(0+4_u_s%&r_m2uo*1tb'
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'Pioneer/media')
MEDIA_URL = '/media/'

