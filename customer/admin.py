from django.contrib import admin

from customer.models import Customer


# Register your models here.
@admin.register(Customer)
class CorporateAdmin(admin.ModelAdmin):
	"""Corporate model admin. Defines the fields to display and which ones are searchable"""
	list_filter = ('date_created', 'country', 'state__name')
	list_display = (
		'name', 'identifier',  'phone_number', 'address', 'postal_code',
		'email_address', 'country', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'remote_code')



