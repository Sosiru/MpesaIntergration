# coding=utf-8
"""
This is the service module from which all CRUD base services are declared.
"""
from django.contrib.auth.models import User

from audit.models import TransactionType, Transaction
from base.backend.servicebase import ServiceBase
from base.models import State, AccountFieldType, Country
# from core.models import AD, ADBid, Category, Location, PasswordToken
# from notifications.models import NotificationBase
from billing.models import PaymentTransaction
# from settings.models import SiteSetting
# from users.models import SheltuzUser
# from orders.models import Order, OrderItem, Cart, Wishlist


class StateService(ServiceBase):
	"""
	State model CRUD services
	"""
	manager = State.objects


class PaymentTransactionService(ServiceBase):
	"""
	PaymentMethod model CRUD services
	"""
	manager = PaymentTransaction.objects


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