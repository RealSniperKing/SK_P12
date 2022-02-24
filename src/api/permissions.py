import copy

from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions


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


# ZERO ACTION
class ZeroDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        #'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

# ONE ACTION
class AddDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        #'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ChangeDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        #'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class DeleteDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        #'GET': ['%(app_label)s.view_%(model_name)s'],
        #'OPTIONS': [],
        #'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ViewDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


# TWO ACTIONS
class AddChangeDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        #'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class AddDeleteDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        #'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class AddViewDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ChangeDeleteDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ChangeViewDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class DeleteViewDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


# THREE ACTIONS
class AddChangeDeleteDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        #'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class AddChangeViewDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class AddDeleteViewDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


# FOUR ACTIONS
class ChangeDeleteViewDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class AddChangeDeleteViewDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }