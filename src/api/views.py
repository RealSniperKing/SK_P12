from django.shortcuts import render
from django.contrib.auth.models import Group

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission, IsAdminUser
from accounts.models import User
from accounts.serializers import UserSerializer, UserSmallSerializer, SignupSerializer, SigninSerializer, UserPutSerializer
from django.contrib.auth import login, authenticate
from crm.models import Client
from crm.serializers import ClientSerializer, ClientDetailSerializer

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import mixins, viewsets
from django.contrib.auth.models import Group
from datetime import timedelta

from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import permissions
from .permissions import ZeroDjangoModelPermissions
from .actions import get_one_action, get_two_actions, get_three_actions, get_four_actions


def get_user_permissions_from_admin_interface(user, model_name):
    print("-------------------------------")
    model_name_lower = model_name.lower()
    all_groups = user.groups.all()
    print("all_groups = ", all_groups)
    print("groupppp = ", user.groups.all())

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
    actions_number = len(actions_string.split("_"))

    print("actions_string = ", actions_string)
    print("actions_number = ", actions_number)

    # DEFAULT : ZERO ACTION
    active_permission = ZeroDjangoModelPermissions
    perm = None

    # GET ACTIONS
    if actions_number == 1:
        perm = get_one_action(actions_string)

    if actions_number == 2:
        perm = get_two_actions(actions_string)

    if actions_number == 3:
        perm = get_three_actions(actions_string)

    if actions_number == 4:
        perm = get_four_actions(actions_string)

    if perm is not None:
        active_permission = perm

    return active_permission


# VIEWS

class SigninViewset(ModelViewSet):
    serializer_class = SigninSerializer
    http_method_names = ['post']

    def get_queryset(self):
        return User.objects.all()

    def create(self, request):
        """Login user"""
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = authenticate(request,
                                email=serializer.validated_data["email"],
                                password=serializer.validated_data["password"])
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(days=0.2))
            data = {'success': True, 'refresh': str(refresh), 'access': str(access_token)}

            # token = Token.objects.get_or_create(user=user)
            # print("token = ", token)
            # print(token.key)
            # data = {'success': True, 'access': str(token.key)}

            return Response(data, status=status.HTTP_200_OK)

        errors = serializer.errors
        errors["success"] = False
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewset(ModelViewSet):
    """ Comments list"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'user_id'  # Use to show detail page

    action_serializers = {
        'create': UserSerializer,
        'retrieve': UserPutSerializer
    }

    def get_serializer_class(self):
        kwargs_dict = self.kwargs
        if "user_id" in kwargs_dict:
            return self.action_serializers["retrieve"]
        return self.action_serializers["create"]

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            new_user = User.objects.create_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"]
            )
            new_user.save()
            return Response({"success": True}, status=status.HTTP_200_OK)

        errors = serializer.errors
        errors["success"] = False
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        print("UPDATE")
        partial = True
        instance = self.get_object()

        # instance.groups.add("read_only")
        # print("instance = ", instance.email)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        group_name_in_field = serializer.validated_data["role"]

        users_in_group = Group.objects.get(name=group_name_in_field).user_set.all()
        print("users_in_group = ", users_in_group)

        instance = serializer.save()

        print("instance = ", instance)
        print('serializer.data["user_id"] = ', serializer.data["user_id"])

        # Get groups
        groups_list = Group.objects.all()
        print("groups_list =", groups_list)

        # Add to group
        user_ob = User.objects.get(user_id=instance.user_id)
        print("user_ob = ", user_ob)

        # Remove all groups for this user
        user_ob.groups.clear()

        # Assign specific group to user
        user_ob.groups.add(Group.objects.get(name=group_name_in_field))


        # contributor_projects = User.objects.filter(user_id=user_id)

        # print("instance = ", instance)
        # instance.groups.add("read_only")

# class MyEndpoint(mixins.ListModelMixin, viewsets.GenericViewSet):
#     permission_classes = [IsAuthenticated, ReadPermission]
#     http_method_names = ['get']
#     # etc


class ClientViewset(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'client_id'  # Use to show detail page
    # queryset = Client.objects.all()

    action_serializers = {
        'create': ClientSerializer,
        'retrieve': ClientDetailSerializer
    }

    def get_serializer_class(self):
        kwargs_dict = self.kwargs
        #if self.request.user.is_staff:
        if "client_id" in kwargs_dict:
            return self.action_serializers["retrieve"]
        return self.action_serializers["create"]

    def get_permissions(self):
        user = self.request.user
        print("user = ", user)
        print(type(user))
        if not user.is_authenticated:
            self.permission_classes = [IsAuthenticated]
            return super(self.__class__, self).get_permissions()

        permission_test = get_user_permissions_from_admin_interface(user, "Client")
        role = user.role

        # if role and role == User.Types.MANAGEMENT:
        self.permission_classes = [IsAuthenticated, permission_test]

        #return super(ClientViewset, self).get_permissions()
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        return Client.objects.all()

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            response = self.perform_create(serializer)
            return response

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = self.request.user
        client = serializer.save(author=user)
        print("client = ", client)

        # client.groups.add("read_only")

        data = {"success": True,
                "client_id": str(client.client_id)}
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        print("UPDATE")
        partial = True
        instance = self.get_object()

        # instance.groups.add("read_only")
        # print("instance = ", instance.email)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        users_in_group = Group.objects.get(name="read_only").user_set.all()
        print("users_in_group = ", users_in_group)
        instance = serializer.save()

        #print("serializer = ", serializer)
        # print(serializer.validated_data["user_id"])

        # contributor_projects = User.objects.filter(user_id=user_id)

        # print("instance = ", instance)
        # instance.groups.add("read_only")

        # send_email_confirmation(user=self.request.user, modified=instance)