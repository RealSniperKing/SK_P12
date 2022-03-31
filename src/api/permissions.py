import copy

from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions
from accounts.models import User, ManagementGroupName
from django.contrib.auth.models import Group

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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

    def has_permission(self, request, view):
        """list permissions"""
        if request.method in view.allowed_methods:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """detail permissions"""
        print("///////////")
        model_name = obj._meta.model.__name__
        print("model_name = ", model_name)
        user = request.user
        if user is None:
            return False

        # Admin permission
        if user.is_admin:
            return True

        # Is management team
        management_group_name = ManagementGroupName.objects.all()
        management_group = None
        if len(management_group_name) == 1:
            management_group_list = Group.objects.filter(name=management_group_name.first().name)
            if not management_group_list:
                management_group = None
            management_group = management_group_list.first()
        group_all = []
        group_all.extend(user.groups.all())
        print("management_group = ", management_group)
        print("group_all = ", group_all)
        if management_group in group_all:
            return True

        print("*********************************")
        print(obj.client_manager)
        logger.error("*********************************")
        logger.error(obj.client_manager)
        logger.error(user)

        # Client permission
        if model_name == "Customer":
            print("obj.client_manager = ", obj.client_manager)
            print("user = ", user)
            return obj.client_manager == user

        # Contract permission
        if model_name == "Contract":
            return obj.contract_manager == user

        # Event permission
        if model_name == "Event":
            return obj.event_manager == user

        return False







