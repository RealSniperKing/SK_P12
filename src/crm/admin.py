from django.contrib import admin
from .models import Customer, Contract, Event
# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'client_id')  # fields to display in the listing
    empty_value_display = '-empty-'        # display value when empty
    list_filter = ()      # enable results filtering
    list_per_page = 25                     # number of items per page
    ordering = ['-updating_time', 'email']       # Default results ordering

    def has_add_permission(self, request, obj=None):
        return request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin


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

    def has_add_permission(self, request, obj=None):
        return request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_id')  # fields to display in the listing
    empty_value_display = '-empty-'        # display value when empty
    list_filter = ()      # enable results filtering
    list_per_page = 25                     # number of items per page
    ordering = ['-updating_time', 'name']       # Default results ordering

    def has_add_permission(self, request, obj=None):
        return request.user.is_admin

    def has_change_permission(self, request, obj=None):
        return request.user.is_admin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_admin

# and register it
admin.site.register(Customer, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
