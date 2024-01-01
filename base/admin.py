from django.contrib import admin
from django.contrib.auth.models import User, Group

from base.models import State, AccountFieldType, Country
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
	"""
	State model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)


@admin.register(AccountFieldType)
class AccountTypeAdmin(admin.ModelAdmin):
	"""
	AccountFieldType model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'state__name')



@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
	"""
	Country model admin. Defines the fields to display and which ones are searchable
	"""
	list_filter = ('date_created',)
	list_display = ('name', 'description', 'state', 'date_modified', 'date_created')
	search_fields = ('name', 'state__name')


