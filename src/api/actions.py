# def convert_actions_to_http_method_list(actions_string):
#     actions_list = actions_string.split("_")
#     http_method_list = []
#     http_method = None
#     for action in actions_list:
#         if action == "add":
#             http_method = "post"
#         elif action == "change":
#             http_method = "put"
#         elif action == "delete":
#             http_method = "delete"
#         elif action == "view":
#             http_method = "get"
#         if http_method:
#             http_method_list.append(http_method)
#     return http_method_list
