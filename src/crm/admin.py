from django.contrib import admin
from .models import Client, Contract, Event
# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'client_id')  # fields to display in the listing
    empty_value_display = '-empty-'        # display value when empty
    list_filter = ()      # enable results filtering
    list_per_page = 25                     # number of items per page
    ordering = ['-updating_time', 'email']       # Default results ordering


class ContractAdmin(admin.ModelAdmin):
    list_display = ('title', 'contract_id')  # fields to display in the listing
    empty_value_display = '-empty-'        # display value when empty
    list_filter = ()      # enable results filtering
    list_per_page = 25                     # number of items per page
    ordering = ['-updating_time', 'title']       # Default results ordering

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["client"].required = False
        form.base_fields["contract_manager"].required = False
        return form


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_id')  # fields to display in the listing
    empty_value_display = '-empty-'        # display value when empty
    list_filter = ()      # enable results filtering
    list_per_page = 25                     # number of items per page
    ordering = ['-updating_time', 'name']       # Default results ordering


# and register it
admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
