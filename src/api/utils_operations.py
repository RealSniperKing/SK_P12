from uuid import UUID


def permissions_from_admin_groups(user, model_name):
    model_name_lower = model_name.lower()

    group_permissions = user.get_group_permissions()

    actions_list = []
    for group_permission in list(group_permissions):
        permission_action_model = group_permission.split(".")[1]
        permission_action_model_split = permission_action_model.split("_")

        action = permission_action_model_split[0]
        model = permission_action_model_split[1]

        if model == model_name_lower:
            actions_list.append(action)

    actions_string = '_'.join(map(str, sorted(actions_list)))
    http_method_list = convert_actions_to_http_method_list(actions_string)

    if user.is_admin:
        http_method_list = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    return http_method_list


def convert_actions_to_http_method_list(actions_string):
    actions_list = actions_string.split("_")
    http_method_list = []
    http_method = None
    for action in actions_list:
        if action == "add":
            http_method = "post"
        elif action == "change":
            http_method = "put"
        elif action == "delete":
            http_method = "delete"
        elif action == "view":
            http_method = "get"
        if http_method:
            http_method_list.append(http_method)
    return http_method_list


def is_valid_uuid(string_value, version=4):
    try:
        uuid = UUID(str(string_value), version=version)
        return uuid
    except ValueError:
        return None




