import copy

from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions
from accounts.models import User, ManagementGroupName

class D7896DjangoModelPermissions(DjangoModelPermissions):
    # def __init__(self):
    #     self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

    # perms_map = {}
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsManagerOrAdminManager(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        model_name = obj._meta.model.__name__
        user = request.user

        # Admin permission
        if user.is_admin:
            return True

        if user in User.objects.filter(groups__name=ManagementGroupName.objects.first().name):
            return True

        # Client permission
        if model_name == "Client":
            return obj.client_manager == user

        # Contract permission
        if model_name == "Contract":
            return obj.contract_manager == user

        # Event permission
        if model_name == "Event":
            return obj.event_manager == user







