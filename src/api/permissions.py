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


class CustomDjangoModelPermissions(DjangoModelPermissions):
    # def __init__(self, parameters):
    #     self.parameters = parameters
    #     # self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

    # perms_map = {}
    perms_map = {
        # 'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class ReadDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        #'POST': ['%(app_label)s.add_%(model_name)s'],
        #'PUT': ['%(app_label)s.change_%(model_name)s'],
        #'PATCH': ['%(app_label)s.change_%(model_name)s'],
        #'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class PostDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
    }


class PutPatchDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
    }


class DeleteDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }