import os
from copy import deepcopy
from postal import Postal
from postal.configuration_base import base_postal_configuration
from postal.carriers.dhl import DHLApi
from postal.carriers.usps import USPSApi
from postal.carriers.fedex import FedExApi
from postal.carriers.ups import UPSApi
from postal.data import Address
from warehouse.usgm import USGMCarrier
from warehouse.default_settings import *

SECRET_KEY = 'ouifbvweoriguwerogie7rh34yg4978y74h24ugb'

fedex_credentials = {
    'key': 'Ths2IuWg40uM5Bb2',
    'account_number': 510087801,
    'password': 'qL2HeRevKUR8BlZuLCZ7AfYfM',
    'meter_number': 118592078
}

usps_credentials = {
    'account_id': 2505571,
    'passphrase': 'UFmr5K9RzN9v',
    'ipa_convert': True,
    'requester_id': 'lxxx'
}

ups_credentials = {
    'username': 'usglobalmail',
    'password': 'Usgm6425',
    #'access_license_number': '8CC44A8B0B5A7866',
    'access_license_number': 'ECEE84C37A0D2EA6',
    'shipper_number': 'X5925Y',
    'auto_time_in_transit': False,
    'test': True,
}
# CELERY STUFF
BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost//'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_ALWAYS_EAGER = True
CELERY_ENABLE_UTC = True
CELERY_INTERVAL_TIME_IN_HOUR = 24
CELERYBEAT_SCHEDULE = {
    'add-daily_at_midnight': {
        'task': 'tasks.add',
        'schedule': crontab(hour=0, minute=0), ## Execute daily at midnight.
        'args': (16, 16)
    },
}

# Some arguments have to be passed to the USGM carrier this way to avoid
# circular dependencies.
usgm_credentials = {
    'unsupported': UNSUPPORTED_METHODS,
    'hidden': NON_PUBLIC_METHODS
}

base_postal_configuration = deepcopy(base_postal_configuration)

base_postal_configuration['enabled_carriers'] = [
    FedExApi, UPSApi, DHLApi, USPSApi, USGMCarrier
]
base_postal_configuration['carrier_inits']['FedEx'] = fedex_credentials
base_postal_configuration['carrier_inits']['UPS'] = ups_credentials
base_postal_configuration['carrier_inits']['DHL'] = dhl_credentials
base_postal_configuration['carrier_inits']['USPS'] = usps_credentials
base_postal_configuration['carrier_inits']['USGM'] = usgm_credentials
base_postal_configuration['timeout'] = 5
base_postal_configuration['shipper_address'] = Address(
        street_lines=['1321 Upland Dr'], city='Houston',
        subdivision='TX', country='US',
        residential=False, contact_name='US Global Mail',
        postal_code='77043', phone_number='2815968965'
)

SETTINGS_PATH = os.path.dirname(os.path.realpath(__file__))

base_postal_configuration['ci_shipper_logo'] = open(os.path.join(SETTINGS_PATH, '..', 'logo.jpg')).read()
base_postal_configuration['ci_signature'] = open(os.path.join(SETTINGS_PATH, '..', 'signature.jpg')).read()
base_postal_configuration['ci_signed_by'] = 'Chris Tatum'

USGM_POSTAL = Postal(base_postal_configuration)

from default_settings import *
from membership.default_settings import *
from billing.default_settings import *

#FLAT_RATE_STORAGE_PRICE = Decimal('0.00')

CIM_API_LOGIN = u'4b7QcT2Q'
CIM_API_KEY = u'4K529W5K2ddCs7E2'


DEBUG = True

TEST_ENVIRONMENT = True

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'development',                      # Or path to database file if using sqlite3.
        'USER': 'development',                      # Not used with sqlite3.
        'PASSWORD': 'sdiuybv3ro8wybrwoeuivbsdfuvb',
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

HIDE_TEST_BROWSER = False

ALLOWED_HOSTS += ('localtest.usglobalmail.com',)
