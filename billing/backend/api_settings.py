from django.conf import settings
from rest_framework.settings import APISettings
from base.backend.service import CustomerService, ClientCredentialsService
from base.backend.utils.common import get_request_data


def get_customer_credentials(request):
    data = get_request_data(request)
    customer_id = data.get('customer_id')
    customer = CustomerService().get(id=customer_id)
    if not customer:
        raise Exception('Customer not found')
    credentials = ClientCredentialsService().get(customer=customer)
    if not credentials:
        raise Exception('Credentials not set')
    MPESA_CONFIG = {
        'CONSUMER_KEY': str(credentials.consumer_key),
        'CONSUMER_SECRET': str(credentials.consumer_secret),
        'CERTIFICATE_FILE': None, # credentials.certificate_file,
        'HOST_NAME': str(credentials.host_name),
        'PASS_KEY': str(credentials.pass_key),
        'SAFARICOM_API': str(credentials.safaricom_api),
        'AUTH_URL': str(credentials.auth_url),
        'SHORT_CODE': str(credentials.short_code),
        'TILL_NUMBER': str(credentials.till_number),
        'TRANSACTION_TYPE': str(credentials.trx_type),
    }
    USER_SETTINGS = getattr(settings, MPESA_CONFIG, None)
    DEFAULTS = {
        'CONSUMER_KEY': None,
        'CONSUMER_SECRET': None,
        'CERTIFICATE_FILE': None,
        'HOST_NAME': None,
        'PASS_KEY': None,
        'SAFARICOM_API': 'https://sandbox.safaricom.co.ke',
        'AUTH_URL': '/oauth/v1/generate?grant_type=client_credentials',
        'SHORT_CODE': None,
        'TILL_NUMBER': None,
        'TRANSACTION_TYPE': 'CustomerBuyGoodsOnline',
    }
    api_settings = APISettings(USER_SETTINGS, DEFAULTS, None)
    return MPESA_CONFIG





