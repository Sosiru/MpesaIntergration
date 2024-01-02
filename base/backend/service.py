# coding=utf-8
"""
This is the service module from which all CRUD base services are declared.
"""
from django.contrib.auth.models import User

from audit.models import TransactionType, Transaction
from base.backend.servicebase import ServiceBase
from base.models import State, AccountFieldType, Country
from billing.models import PaymentTransaction, ClientCredentials
from customer.models import Customer


class StateService(ServiceBase):
	"""
	State model CRUD services
	"""
	manager = State.objects


class PaymentTransactionService(ServiceBase):
	"""
	Payment Transactions model CRUD services
	"""
	manager = PaymentTransaction.objects


class CustomerService(ServiceBase):
	"""
	Customer  model CRUD services
	"""
	manager = Customer.objects


class CustomerCredentialService(ServiceBase):
	"""
	Customer Credentials  model CRUD services
	"""
	manager = ClientCredentials.objects


class AccountFieldTypeService(ServiceBase):
	"""
	AccountFieldType model CRUD services
	"""
	manager = AccountFieldType.objects


class CountryService(ServiceBase):
	"""
	Country model CRUD services
	"""
	manager = Country.objects


class TransactionTypeService(ServiceBase):
	"""
	TransactionType model CRUD services
	"""
	manager = TransactionType.objects


class TransactionService(ServiceBase):
	"""
	Transaction model CRUD services
	"""
	manager = Transaction.objects