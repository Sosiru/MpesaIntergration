# 300
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction as trx

from audit.models import TransactionType
from base.backend.utils.common import disable_for_loaddata
from base.models import BaseModel, State, Country, GenericBaseModel


# 01
class Customer(BaseModel):
	name = models.CharField(max_length=50)
	identifier = models.CharField(max_length=50, unique=True)
	phone_number = models.CharField(max_length=50, null=True, blank=True)
	email_address = models.CharField(max_length=50, null=True, blank=True)
	address = models.CharField(max_length=50, null=True, blank=True)
	postal_code = models.CharField(max_length=50, null=True, blank=True)
	country = models.ForeignKey(Country, default=Country.default_country(),on_delete=models.CASCADE)
	state = models.ForeignKey(State, default=State.default_state, on_delete=models.CASCADE)

	def __str__(self):
		return '%s - %s' % (self.name, self.country.name)

	class Meta:
		verbose_name_plural = "Customer"
		ordering = ['-date_created']




# 04
