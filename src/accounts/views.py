# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission, IsAdminUser
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.views import APIView
# from rest_framework.exceptions import NotFound
#
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.models import Group
# from django_filters.rest_framework import DjangoFilterBackend
#
# from .models import User
# from .serializers import UserSerializer, SignupSerializer, SigninSerializer, UserDetailSerializer
# from datetime import timedelta
#
#
# def permissions_from_admin_groups(user, model_name):
#     print("-------------------------------")
#     print(user)
#     model_name_lower = model_name.lower()
#     all_groups = user.groups.all()
#     print("all_groups = ", all_groups)
#     print("groupppp = ", user.groups.all())
#
#     group_permissions = user.get_group_permissions()
#
#     actions_list = []
#     for group_permission in list(group_permissions):
#         permission_action_model = group_permission.split(".")[1]
#         permission_action_model_split = permission_action_model.split("_")
#
#         action = permission_action_model_split[0]
#         model = permission_action_model_split[1]
#
#         if model == model_name_lower:
#             actions_list.append(action)
#
#     actions_string = '_'.join(map(str, sorted(actions_list)))
#     print("actions_string = ", actions_string)
#     http_method_list = convert_actions_to_http_method_list(actions_string)
#
#     if user.is_admin:
#         #'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'
#         http_method_list = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
#
#     return http_method_list
#
# # USERS
# class SigninViewset(ModelViewSet):
#     serializer_class = SigninSerializer
#     http_method_names = ['post']
#     permission_classes = []
#
#     def get_queryset(self):
#         return User.objects.all()
#
#     def create(self, request):
#         """Login user"""
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#
#         if serializer.is_valid():
#             user = authenticate(request,
#                                 email=serializer.validated_data["email"],
#                                 password=serializer.validated_data["password"])
#             login(request, user)
#
#             refresh = RefreshToken.for_user(user)
#             access_token = refresh.access_token
#             access_token.set_exp(lifetime=timedelta(days=0.2))
#             data = {'success': True, 'refresh': str(refresh), 'access': str(access_token)}
#
#             # token = Token.objects.get_or_create(user=user)
#             # print("token = ", token)
#             # print(token.key)
#             # data = {'success': True, 'access': str(token.key)}
#
#             return Response(data, status=status.HTTP_200_OK)
#
#         errors = serializer.errors
#         errors["success"] = False
#         return Response(errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SignoutViewset(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         """Logout"""
#         print(request.user)
#         logout(request)
#         return Response({"success": True}, status=status.HTTP_200_OK)
#
#
# class UserViewset(ModelViewSet):
#     """ Comments list"""
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = []
#     lookup_field = 'user_id'  # Use to show detail page
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['email', 'groups']
#
#     action_serializers = {
#         'create': UserSerializer,
#         'retrieve': UserDetailSerializer
#     }
#
#     def get_serializer_class(self):
#         kwargs_dict = self.kwargs
#         if "user_id" in kwargs_dict:
#             return self.action_serializers["retrieve"]
#         return self.action_serializers["create"]
#
#     def get_permissions(self):
#         user = self.request.user
#         if not user.is_authenticated:
#             self.permission_classes = [IsAuthenticated]
#             return super(self.__class__, self).get_permissions()
#
#         http_method_list = permissions_from_admin_groups(user, "User")
#         self.http_method_names = http_method_list
#
#         return super(self.__class__, self).get_permissions()
#
#     def dispatch(self, *args, **kwargs):
#         """Use dispatch to update http_method_names"""
#         response = super(UserViewset, self).dispatch(*args, **kwargs)
#         # response['Cache-Control'] = 'no-cache'
#         response['Allow'] = ', '.join(self.http_method_names)
#         return response
#
#     def get_queryset(self):
#         return User.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#
#         if serializer.is_valid():
#             new_user = User.objects.create_user(
#                 email=serializer.validated_data["email"],
#                 password=serializer.validated_data["password"],
#             )
#             new_user.save()
#             # group_name = serializer.validated_data["role"]
#             # if group_name:
#             #     new_user.groups.add(Group.objects.get(name=serializer.validated_data["role"]))
#             # return Response({"success": True, "user_id": new_user.user_id}, status=status.HTTP_200_OK)
#
#         errors = serializer.errors
#         errors["success"] = False
#         return Response(errors, status.HTTP_400_BAD_REQUEST)
#
#     def update(self, request, *args, **kwargs):
#         print("UPDATE")
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#
#         print("serializer = ", serializer)
#
#         if serializer.is_valid():
#             # print(serializer.validated_data["groups"])
#             # print(serializer.validated_data["group_name"])
#             # serializer.is_valid(raise_exception=True)
#             # serializer.validated_data["groups"] = serializer.validated_data["group_name"]
#             self.perform_update(serializer)
#             return Response(serializer.data)
#
#         errors = serializer.errors
#         errors["success"] = False
#         return Response(errors, status.HTTP_400_BAD_REQUEST)
#
#     def perform_update(self, serializer):
#         # group_name_in_field = serializer.validated_data["role"]
#         #
#         # users_in_group = Group.objects.get(name=group_name_in_field).user_set.all()
#         # print("users_in_group = ", users_in_group)
#         instance = serializer.save()
#
#         # user_ob = User.objects.get(user_id=instance.user_id)
#         # role_field = "role"
#         # if role_field in serializer.validated_data:
#         #     group_name = serializer.validated_data[role_field]
#         #     if group_name:
#         #         user_ob.groups.clear()
#         #         user_ob.groups.add(Group.objects.get(name=serializer.validated_data["role"]))
#
#         # errors = serializer.errors
#         # errors["success"] = False
#         # return Response(errors, status.HTTP_400_BAD_REQUEST)