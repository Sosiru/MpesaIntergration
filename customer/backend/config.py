from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from base.backend.service import CustomerService, StateService, CustomerCredentialService
from base.backend.utils.common import get_request_data
from rest_framework.settings import APISettings
# Create your views here.


class CustomerManagement(object):
	@csrf_exempt
	@staticmethod
	def onboard(request):
		"""Onboards a customer to start using MPESA STK"""
		try:

			data = get_request_data(request)
			name = data.get('name')
			identifier = data.get("identifier")
			phone_number = data.get("phone_number")
			email = data.get("email")
			address = data.get("address")
			postal_code = data.get('postal_code')
			if not any([name, identifier]):
				return JsonResponse({"code": "403.001", "message": "Customer name, and key required."})
			customer = CustomerService().filter(name=name, identifier=identifier).first()
			if customer:
				customer = CustomerService().update(pk=customer.id, state=StateService().get(name="Active"))
			else:
				customer = CustomerService().create(
					name=name, identifier=identifier, phone_number=phone_number,
					email_address=email, address=address, postal_code=postal_code,
					state=StateService().get(name="Active"))
			if not customer:
				return JsonResponse({"code": "500.001", "message": "error creating corporate"})
			return JsonResponse({"code": "200.001"})
		except Exception as e:
			print(e)
		return JsonResponse({"code": "500.001", "message": "Exception while searching"})

	@staticmethod
	@csrf_exempt
	def get_customer_stage_credentials(**data):
		"""Fetches customer_credentials a customer to start using MPESA STK"""
		try:
			customer_identifier = data.get('identifier')
			customer = CustomerService().get(identifier=customer_identifier)
			if not customer:
				return JsonResponse({"code": "403.001", "message": "Customer not found"})
			credentials = CustomerCredentialService().get(customer=customer, environment="STAGE",state=StateService().get(name="Active"))
			if not credentials:
				return JsonResponse({"code": "403.001", "message": "Credentials not found"})

			MPESA_CONFIG = {
				'CONSUMER_KEY': str(credentials.consumer_key),
				'CONSUMER_SECRET': str(credentials.consumer_secret),
				# 'CERTIFICATE_FILE': ,
				'HOST_NAME': str(credentials.host_name),
				'PASS_KEY': str(credentials.pass_key),
				'SAFARICOM_API': str(credentials.safaricom_api),
				'AUTH_URL': str(credentials.auth_url),
				'SHORT_CODE': str(credentials.shortcode),
				'TILL_NUMBER':str(credentials.till_number),
				'TRANSACTION_TYPE': str(credentials.trx_type),
			}
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

			api_settings = APISettings(MPESA_CONFIG, DEFAULTS, None)
			return api_settings
		except Exception as e:
			print(e)
			return JsonResponse({"code": "500.001", "message": "Credentials not valid"})


	@staticmethod
	@csrf_exempt
	def create_customer_stage_credentials(request):
		"""Fetches customer_credentials a customer to start using MPESA STK"""
		try:

			data = get_request_data(request)
			customer_identifier = data.get('identifier')
			customer = CustomerService().get(identifier=customer_identifier)
			if not customer:
				return JsonResponse({"code": "403.001", "message": "Customer not found"})
			credentials = CustomerCredentialService().get(customer=customer, environment="STAGE",state=StateService().get(name="Active"))
			if not credentials:
				return JsonResponse({"code": "403.001", "message": "Credentials not found"})
			MPESA_CONFIG = {
				'CONSUMER_KEY': str(credentials.consumer_key),
				'CONSUMER_SECRET': str(credentials.consumer_secret),
				# 'CERTIFICATE_FILE': ,
				'HOST_NAME': str(credentials.host_name),
				'PASS_KEY': str(credentials.pass_key),
				'SAFARICOM_API': str(credentials.safaricom_api),
				'AUTH_URL': str(credentials.auth_url),
				'SHORT_CODE': str(credentials.shortcode),
				'TILL_NUMBER':str(credentials.till_number),
				'TRANSACTION_TYPE': str(credentials.trx_type),
			}

			return JsonResponse({"code": "200.001", "MPESA_CONFIG": MPESA_CONFIG})
		except Exception as e:
			print(e)
			return JsonResponse({"code": "500.001", "message": "Credentials not valid"})


	@staticmethod
	@csrf_exempt
	def create_customer_prod_credentials(request):
		"""Creates customer_credentials a customer to start using MPESA STK"""
		try:
			data = get_request_data(request)
			auth_url = data.get('auth_url')
			consumer_key = data.get('consumer_key')
			safaricom_api = data.get('safaricom_api')
			host_name = data.get('host_name')
			account_number = data.get('account_number')
			till_number = data.get('till_number')
			trx_type = data.get('trx_type')
			customer_identifier = data.get('identifier')
			customer = CustomerService().get(identifier=customer_identifier)
			if not customer:
				return JsonResponse({"code": "403.001", "message": "Customer not found"})
			credentials = CustomerCredentialService().create(
				customer=customer, environment="PRODUCTION", trx_type=trx_type,
				till_number=till_number, account_number=account_number,
				host_name=host_name, safaricom_api=safaricom_api, consumer_key=consumer_key,
				auth_url=auth_url,
				state=StateService().get(name="Active"))
			if not credentials:
				return JsonResponse({"code": "403.001", "message": "Error!"})
			return JsonResponse({"code": "200.001"})
		except Exception as e:
			print(e)
			return JsonResponse({"code": "500.001", "message": "Credentials not valid"})


	@staticmethod
	@csrf_exempt
	def create_customer_stage_credentials(request):
		"""Creates customer_credentials a customer to start using MPESA STK"""
		try:
			data = get_request_data(request)
			auth_url = data.get('auth_url')
			consumer_key = data.get('consumer_key')
			safaricom_api = data.get('safaricom_api')
			host_name = data.get('host_name')
			account_number = data.get('account_number')
			till_number = data.get('till_number')
			trx_type = data.get('trx_type')
			customer_identifier = data.get('identifier')
			customer = CustomerService().get(identifier=customer_identifier)
			if not customer:
				return JsonResponse({"code": "403.001", "message": "Customer not found"})
			credentials = CustomerCredentialService().create(
				customer=customer, environment="STAGE", trx_type=trx_type,
				till_number=till_number, account_number=account_number,
				host_name=host_name, safaricom_api=safaricom_api, consumer_key=consumer_key,
				auth_url=auth_url,
				state=StateService().get(name="Active"))
			if not credentials:
				return JsonResponse({"code": "403.001", "message": "Error!"})
			return JsonResponse({"code": "200.001"})
		except Exception as e:
			print(e)
			return JsonResponse({"code": "500.001", "message": "Credentials not valid"})


