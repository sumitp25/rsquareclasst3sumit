from decouple import config

ENVIRONMENT = config('ENVIRONMENT', default='local')
# ENVIRONMENT = 'local'
# ENVIRONMENT = 'development'
# ENVIRONMENT = 'production'

SETTINGS_MODULE = 'rsquareclass.local'

if ENVIRONMENT == 'local':
    SETTINGS_MODULE = 'rsquareclass.local'
if ENVIRONMENT == 'heroku':
    SETTINGS_MODULE = 'rsquareclass.heroku'

