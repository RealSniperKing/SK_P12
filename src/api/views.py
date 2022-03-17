from django.shortcuts import redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponseNotFound
from django.http import Http404
import json
from accounts.models import User
from accounts.serializers import UserSerializer, SignupSerializer, SigninSerializer, UserDetailSerializer

from crm.models import Customer, Contract, Event
from crm.serializers import ClientSerializer, ClientDetailSerializer, \
    ContractSerializer, ContractDetailSerializer, EventSerializer

from .permissions import IsManagerOrAdminManager
from .actions import convert_actions_to_http_method_list

from datetime import timedelta

# import the logging library
import logging, logging.handlers
from .utils_operations import is_valid_uuid
# Get an instance of a logger
logger = logging.getLogger(__name__)


def permissions_from_admin_groups(user, model_name):
    print("-------------------------------")
    print(user)
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
    print("actions_string = ", actions_string)
    http_method_list = convert_actions_to_http_method_list(actions_string)

    if user.is_admin:
        #'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'
        http_method_list = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    return http_method_list


def error500(request):
    print("------------- Test error 500 -------------")
    raise NotFound(detail="Fatal error", code=500)


# def error404(request, exception):
#     response_data = {}
#     response_data['detail'] = 'Not found.'
#     return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")

    # logger.error(request.data)
    # raise NotFound(detail="Error 404", code=404)


def error404(request):
    print("------------- Error -------------")
    logger.error(request.data)
    raise NotFound(detail="Error 404, page not found", code=404)


# USERS
class SigninViewset(ModelViewSet):
    serializer_class = SigninSerializer
    http_method_names = ['post']
    permission_classes = []

    def get_queryset(self):
        # try:
        return User.objects.all()
        # except Exception as e:
        #     logger.error(f"error = {self.request}")
        #     logger.error(f"error = {e}")
        #     return None

    def create(self, request):
        """Login user"""
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                logger.error(f"request = {self.request}")
                logger.error(f"email = {serializer.validated_data['email']}")
                logger.error(f"password = {serializer.validated_data['password']}")
                user = User.objects.filter(email=serializer.validated_data['email']).first()
                # user = authenticate(request,
                #                     email=serializer.validated_data["email"],
                #                     password=serializer.validated_data["password"])
                if user.is_active:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    access_token = refresh.access_token
                    access_token.set_exp(lifetime=timedelta(days=0.2))

                    data = {'success': True, 'refresh': str(refresh), 'access': str(access_token)}
                    logger.error(f"data = {data}")
                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        errors = serializer.errors
        errors["success"] = False
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class SignoutViewset(APIView):
    #IsAuthenticated
    permission_classes = []

    def get(self, request, format=None):
        """Logout"""
        try:
            # request = "dd"
            logout(request)
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"request = {self.request}")
            logger.error(f"error = {e}")
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)


class UserViewset(ModelViewSet):
    """ Comments list"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = []
    lookup_field = 'user_id'  # Use to show detail page
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'groups']

    action_serializers = {
        'create': UserSerializer,
        'retrieve': UserDetailSerializer
    }

    def get_serializer_class(self):
        kwargs_dict = self.kwargs
        if "user_id" in kwargs_dict:
            return self.action_serializers["retrieve"]
        return self.action_serializers["create"]

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            self.permission_classes = [IsAuthenticated]
            return super(self.__class__, self).get_permissions()

        http_method_list = permissions_from_admin_groups(user, "User")
        self.http_method_names = http_method_list

        return super(self.__class__, self).get_permissions()

    def dispatch(self, *args, **kwargs):
        """Use dispatch to update http_method_names"""
        response = super(UserViewset, self).dispatch(*args, **kwargs)
        # response['Cache-Control'] = 'no-cache'
        response['Allow'] = ', '.join(self.http_method_names)
        return response

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                new_user = User.objects.create_user(
                    email=serializer.validated_data["email"],
                    password=serializer.validated_data["password"],
                )
                new_user.save()
                return Response({"success": True, "user_id": new_user.user_id}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        errors = serializer.errors
        errors["success"] = False
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            try:
                self.perform_update(serializer)
                return Response(serializer.data)
            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        errors = serializer.errors
        errors["success"] = False
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = serializer.save()

        # user_ob = User.objects.get(user_id=instance.user_id)
        # role_field = "role"
        # if role_field in serializer.validated_data:
        #     group_name = serializer.validated_data[role_field]
        #     if group_name:
        #         user_ob.groups.clear()
        #         user_ob.groups.add(Group.objects.get(name=serializer.validated_data["role"]))

        # errors = serializer.errors
        # errors["success"] = False
        # return Response(errors, status.HTTP_400_BAD_REQUEST)


# CLIENTS
class ClientViewset(ModelViewSet):
    serializer_class = ClientSerializer
    #IsAuthenticated, IsManagerOrAdminManager
    permission_classes = []
    http_method_names = []
    lookup_field = 'client_id'  # Use to show detail page
    # queryset = Customer.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_name', 'client_id', 'client_manager']

    action_serializers = {
        'create': ClientSerializer,
        'retrieve': ClientDetailSerializer
    }

    def get_serializer_class(self):
        kwargs_dict = self.kwargs
        #if self.request.user.is_staff:

        id_name = "client_id"
        if id_name in kwargs_dict:
            return self.action_serializers["retrieve"]
        return self.action_serializers["create"]

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            self.permission_classes = [IsAuthenticated]
            return super(self.__class__, self).get_permissions()

        http_method_list = permissions_from_admin_groups(user, "Customer")

        self.http_method_names = http_method_list

        return super(self.__class__, self).get_permissions()

    def dispatch(self, *args, **kwargs):
        """Use dispatch to update http_method_names"""
        response = super(ClientViewset, self).dispatch(*args, **kwargs)
        # response['Cache-Control'] = 'no-cache'
        response['Allow'] = ', '.join(self.http_method_names)
        return response

    def get_queryset(self):
        groups_list = Group.objects.all()
        print("groups_list =", groups_list)

        group_name = Group.objects.filter(name='Equipe de vente')
        print("group_name = ", group_name)

        print(User.objects.filter(groups__name='Equipe de vente'))

        return Customer.objects.all()

    # def retrieve(self, request, *args, **kwargs):
    #     print("//////////")
    #     kwargs_dict = self.kwargs
    #     id_name = "client_id"
    #     if id_name in kwargs_dict:
    #         client_id = kwargs_dict[id_name]
    #         client_uuid = is_valid_uuid(client_id)
    #         print("client_uuid = ", client_uuid)
    #         if not client_uuid:
    #             print("no uuid")
    #             return error404(self.request)

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

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()


# CONTRACTS
class ContractViewset(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdminManager]
    http_method_names = []
    lookup_field = 'contract_id'  # Use to show detail page
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'client', 'contract_manager']

    action_serializers = {
        'create': ContractSerializer,
        'retrieve': ContractDetailSerializer
    }

    def get_serializer_class(self):
        kwargs_dict = self.kwargs
        if "contract_id" in kwargs_dict:
            return self.action_serializers["retrieve"]
        return self.action_serializers["create"]

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            self.permission_classes = [IsAuthenticated]
            return super(self.__class__, self).get_permissions()

        http_method_list = permissions_from_admin_groups(user, "Contract")
        self.http_method_names = http_method_list

        return super(self.__class__, self).get_permissions()

    def dispatch(self, *args, **kwargs):
        """Use dispatch to update http_method_names"""
        response = super(ContractViewset, self).dispatch(*args, **kwargs)
        print("--------")
        # response['Cache-Control'] = 'no-cache'
        response['Allow'] = ', '.join(self.http_method_names)
        return response

    def get_queryset(self):
        return Contract.objects.all()


# EVENTS
class EventViewset(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdminManager]
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'event_id'  # Use to show detail page
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['company_name']

    action_serializers = {
        'create': EventSerializer,
        'retrieve': EventSerializer
    }

    def get_serializer_class(self):
        kwargs_dict = self.kwargs
        #if self.request.user.is_staff:
        if "client_id" in kwargs_dict:
            return self.action_serializers["retrieve"]
        return self.action_serializers["create"]

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            self.permission_classes = [IsAuthenticated]
            return super(self.__class__, self).get_permissions()

        http_method_list = permissions_from_admin_groups(user, "Event")
        self.http_method_names = http_method_list

        return super(self.__class__, self).get_permissions()

    def dispatch(self, *args, **kwargs):
        """Use dispatch to update http_method_names"""
        response = super(EventViewset, self).dispatch(*args, **kwargs)
        # response['Cache-Control'] = 'no-cache'
        response['Allow'] = ', '.join(self.http_method_names)
        return response

    def get_queryset(self):

        return Event.objects.all()