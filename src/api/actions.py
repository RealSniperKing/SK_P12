from .permissions import *


def get_one_action(actions_string):
    active_permission = None
    if actions_string == "add":
        active_permission = AddDjangoModelPermissions
    elif actions_string == "change":
        active_permission = ChangeDjangoModelPermissions
    elif actions_string == "delete":
        active_permission = DeleteDjangoModelPermissions
    elif actions_string == "view":
        active_permission = ViewDjangoModelPermissions
    return active_permission


def get_two_actions(actions_string):
    active_permission = None
    if actions_string == "add_change":
        active_permission = AddChangeDjangoModelPermissions
    elif actions_string == "add_delete":
        active_permission = AddDeleteDjangoModelPermissions
    elif actions_string == "add_view":
        active_permission = AddViewDjangoModelPermissions
    elif actions_string == "change_delete":
        active_permission = ChangeDeleteDjangoModelPermissions
    elif actions_string == "change_view":
        active_permission = ChangeViewDjangoModelPermissions
    elif actions_string == "delete_view":
        active_permission = DeleteViewDjangoModelPermissions
    return active_permission


def get_three_actions(actions_string):
    active_permission = None
    if actions_string == "add_change_delete":
        active_permission = AddChangeDeleteDjangoModelPermissions
    elif actions_string == "add_change_view":
        active_permission = AddChangeViewDjangoModelPermissions
    elif actions_string == "add_delete_view":
        active_permission = AddDeleteViewDjangoModelPermissions
    return active_permission


def get_four_actions(actions_string):
    active_permission = None
    if actions_string == "change_delete_view":
        active_permission = ChangeDeleteViewDjangoModelPermissions
    elif actions_string == "add_change_delete_view":
        active_permission = AddChangeDeleteViewDjangoModelPermissions
    return active_permission
