from django.db import models, transaction

from base.models import GenericBaseModel, State, BaseModel
from base.backend.utils.common import generate_internal_reference

# Create your models here.


class TransactionType(GenericBaseModel):
	"""
	Transaction type model e.g. "WalletLoad", "WalletSpend"
	"""
	simple_name = models.CharField(max_length=50)
	is_viewable = models.BooleanField(default=False)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return '%s %s' % (self.name, self.simple_name)

	class Meta(GenericBaseModel.Meta):
		unique_together = ('name',)


class Transaction(BaseModel):
	"""
	The transactions happening in the system. e.g. Register,Deposit,
	"""
	transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
	reference = models.CharField(max_length=100, null=True, blank=True)
	source_ip = models.CharField(max_length=30, null=True, blank=True)
	request = models.TextField(null=True, blank=True)
	response = models.TextField(null=True, blank=True)
	description = models.TextField(max_length=300, null=True, blank=True)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	SYNC_MODEL = False

	def __str__(self):
		return '%s %s' % (self.transaction_type, self.reference)

	@classmethod
	def next_reference(cls, retries=0):
		"""
		Retrieves the current transaction in the DB to pass to the generator after locking the selected ID.
		This then attempts to generate a unique reference for use with the next transaction.
		@param retries: The number of times we have retried generating a unique reference.
		@type retries: int
		@return: The generated Reference.
		@rtype: str | None
		"""
		with transaction.atomic():
			last_trx = cls.objects.select_for_update().order_by('-date_created').first()
			ref = generate_internal_reference(last_trx.reference if last_trx else None)
			if cls.objects.filter(reference=ref).exists() and retries < 20:
				retries += 1
				return cls.next_reference(retries)
			return ref

	def save(self, *args, **kwargs):
		self.reference = self.next_reference()
		super(Transaction, self).save(*args, **kwargs)
