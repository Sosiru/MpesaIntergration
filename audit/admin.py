from django.contrib import admin

from audit.models import TransactionType, Transaction


# Register your models here.

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
	"""
	The transactiontype admin model.
	"""
	list_filter = ('date_created',)
	ordering = ('-date_created',)
	list_display = (
		'name', 'simple_name', 'description', 'state', 'date_modified', 'date_created')
	search_fields = (
		'name', 'state__name')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	"""
	The transaction admin model.
	"""
	list_filter = ('date_created',)
	ordering = ('-date_created',)
	list_display = (
		'transaction_type', 'reference', 'source_ip', 'request', 'response', 'description',
		'state', 'date_modified', 'date_created')
	search_fields = (
		'transaction_type__name', 'reference', 'state__name')