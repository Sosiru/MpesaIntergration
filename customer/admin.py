from django.contrib import admin

from customer.models import Customer, CustomerAccount, Service


# Register your models here.
@admin.register(Customer)
class CorporateAdmin(admin.ModelAdmin):
	"""Corporate model admin. Defines the fields to display and which ones are searchable"""
	list_filter = ('date_created', 'country', 'state__name')
	list_display = (
		'name', 'identifier',  'phone_number', 'address', 'postal_code',
		'email_address', 'country', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'remote_code')


@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
	"""CorporateAccount model admin. Defines the fields to display and which ones are searchable"""
	list_filter = ('date_created', 'customer__country', 'state')
	list_display = (
		'customer', 'account_number', 'state',
		'date_modified', 'date_created')
	search_fields = ('name', 'account_number', 'corporate__name')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	"""DocumentProcessed model admin. Defines the fields to display and which ones are searchable"""
	list_filter = ('date_created', 'state')
	list_display = ('service_id', 'state', 'date_modified', 'date_created')
	search_fields = ('service_id', 'state__name')


