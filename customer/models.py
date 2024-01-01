# 300
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction as trx

from audit.models import TransactionType
from base.backend.utils.common import disable_for_loaddata
from base.models import BaseModel, State, Country, GenericBaseModel


# 01
# Create your models here.
class Customer(BaseModel):
	name = models.CharField(max_length=50)
	identifier = models.CharField(max_length=50, unique=True)
	phone_number = models.CharField(max_length=50, null=True, blank=True)
	email_address = models.CharField(max_length=50, null=True, blank=True)
	address = models.CharField(max_length=50, null=True, blank=True)
	postal_code = models.CharField(max_length=50, null=True, blank=True)
	country = models.ForeignKey(Country, on_delete=models.CASCADE)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return '%s - %s' % (self.name, self.country.name)

	class Meta:
		verbose_name_plural = "Customer"
		ordering = ['-date_created']


# 02
class CustomerAccount(BaseModel):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	account_number = models.CharField(max_length=50, default=1000000000)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return '%s  %s' % (self.customer, self.account_number)

	class Meta:
		verbose_name_plural = "Customer Account"
		ordering = ['-date_created']

	@receiver(post_save, sender=customer)
	@disable_for_loaddata
	def create_corporate_account(sender, instance, created, **kwargs):
		"""Sends a signal for default account to be generated when a customer is created"""
		with trx.atomic():
			acc = CustomerAccount.objects.select_for_update().order_by('-date_created').first()
			accno = str(int(acc.account_number) + 1) if acc else "100000000"

		if created:
			CustomerAccount.objects.create(corporate=instance, account_number=accno, state=instance.state)


# 03
class Service(GenericBaseModel):
	customer = models.ForeignKey(Customer, null=False, blank=False, on_delete=models.CASCADE)
	service_id = models.CharField(max_length=100, unique=True)
	amount = models.DecimalField(decimal_places=2, max_digits=25, null=True, blank=True)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return '%s  %s' % (self.service_id, self.state)

	class Meta:
		verbose_name_plural = "Service"
		ordering = ['-date_created']


# 04
