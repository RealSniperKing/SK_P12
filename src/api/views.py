from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.contrib.auth import login, authenticate, logout
from django_filters.rest_framework import DjangoFilterBackend

from django_filters import rest_framework as restfilters
from accounts.models import User
from accounts.serializers import UserSerializer, SignupSerializer, SigninSerializer, UserDetailSerializer

from crm.models import Customer, Contract, Event
from crm.serializers import ClientSerializer, ClientDetailSerializer, \
    ContractSerializer, ContractDetailSerializer, EventSerializer

from .permissions import IsManagerOrAdminManager
from .utils_operations import permissions_from_admin_groups

from datetime import timedelta

# import the logging library
import logging, logging.handlers

# Get an instance of a logger
logger = logging.getLogger(__name__)


def error500(request):
    print("------------- Test error 500 -------------")
    raise NotFound(detail="Fatal error", code=500)


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
        return None

    def create(self, request):
        """Login user"""
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                logger.error(f"request = {self.request}")
                logger.error(f"email = {serializer.validated_data['email']}")
                logger.error(f"password = {serializer.validated_data['password']}")

                user = authenticate(request,
                                    email=serializer.validated_data['email'],
                                    password=serializer.validated_data['password'])

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

    def list(self, request, *args, **kwargs):
        return Response({"success": False}, status.HTTP_400_BAD_REQUEST)


class SignoutViewset(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Logout"""
        try:
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
    filterset_fields = ['email', 'groups__name']

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

        http_method_list = permissions_from_admin_groups(user, User.__name__)
        self.http_method_names = http_method_list

        return super(self.__class__, self).get_permissions()

    def dispatch(self, *args, **kwargs):
        """Use dispatch to update http_method_names"""
        response = super(UserViewset, self).dispatch(*args, **kwargs)
        response['Allow'] = ', '.join(self.http_method_names)
        return response

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            # pagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({"success": True, "data": serializer.data})

            serializer = self.action_serializers["create"](queryset, many=True)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

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
        logger.error(f"error = {serializer.errors}")
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            try:
                return self.perform_update(serializer)
            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        errors = serializer.errors
        errors["success"] = False
        logger.error(f"error = {serializer.errors}")
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = serializer.save()
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            ob = self.get_object()
            ob.delete()
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)


# CLIENTS
class ClientViewset(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdminManager]
    http_method_names = []
    lookup_field = 'client_id'  # Use to show detail page
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_name', 'client_manager__email']

    action_serializers = {
        'create': ClientSerializer,
        'retrieve': ClientDetailSerializer
    }

    def get_serializer_class(self):
        kwargs_dict = self.kwargs

        id_name = "client_id"
        if id_name in kwargs_dict:
            return self.action_serializers["retrieve"]
        return self.action_serializers["create"]

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            self.permission_classes = [IsAuthenticated]
            return super(self.__class__, self).get_permissions()

        http_method_list = permissions_from_admin_groups(user, Customer.__name__)

        self.http_method_names = http_method_list

        return super(self.__class__, self).get_permissions()

    def dispatch(self, *args, **kwargs):
        """Use dispatch to update http_method_names"""
        response = super(ClientViewset, self).dispatch(*args, **kwargs)
        response['Allow'] = ', '.join(self.http_method_names)
        return response

    def get_queryset(self):
        return Customer.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            # pagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({"success": True, "data": serializer.data})

            serializer = self.action_serializers["create"](queryset, many=True)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                response = self.perform_create(serializer)
                return response
            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        errors = serializer.errors
        errors["success"] = False
        logger.error(f"error = {serializer.errors}")
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = self.request.user
        client = serializer.save(author=user)
        print("client = ", client)

        data = {"success": True,
                "client_id": str(client.client_id)}
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        # serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            try:
                return self.perform_update(serializer)
            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        errors = serializer.errors
        errors["success"] = False
        logger.error(f"error = {serializer.errors}")
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = serializer.save()
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            ob = self.get_object()
            ob.delete()
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)


# CONTRACTS
class ContractFilter(restfilters.FilterSet):
    is_null_client = restfilters.BooleanFilter(field_name='client', lookup_expr='isnull')
    is_null_manager = restfilters.BooleanFilter(field_name='contract_manager__email', lookup_expr='isnull')

    class Meta:
        model = Contract
        fields = ('title', 'client__company_name', 'contract_manager__email')


class ContractViewset(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdminManager]
    http_method_names = []
    lookup_field = 'contract_id'  # Use to show detail page
    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['title', 'client__company_name', 'contract_manager__email', 'contract_manager']
    filterset_class = ContractFilter

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

        http_method_list = permissions_from_admin_groups(user, Contract.__name__)
        self.http_method_names = http_method_list

        return super(self.__class__, self).get_permissions()

    def dispatch(self, *args, **kwargs):
        """Use dispatch to update http_method_names"""
        response = super(ContractViewset, self).dispatch(*args, **kwargs)
        response['Allow'] = ', '.join(self.http_method_names)
        return response

    def get_queryset(self):
        return Contract.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            # pagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({"success": True, "data": serializer.data})

            serializer = self.action_serializers["create"](queryset, many=True)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                response = self.perform_create(serializer)
                return response
            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        errors = serializer.errors
        errors["success"] = False
        logger.error(f"error = {serializer.errors}")
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = self.request.user
        contract = serializer.save()

        data = {"success": True,
                "contract_id": str(contract.contract_id)}
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            try:
                return self.perform_update(serializer)
            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        errors = serializer.errors
        errors["success"] = False
        logger.error(f"error = {serializer.errors}")
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = serializer.save()
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            ob = self.get_object()
            ob.delete()
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)


# EVENTS
class EventViewset(ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdminManager]
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'event_id'  # Use to show detail page
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'event_manager__email']

    action_serializers = {
        'create': EventSerializer,
        'retrieve': EventSerializer
    }

    def get_serializer_class(self):
        kwargs_dict = self.kwargs
        if "client_id" in kwargs_dict:
            return self.action_serializers["retrieve"]
        return self.action_serializers["create"]

    def get_permissions(self):
        user = self.request.user
        if not user.is_authenticated:
            self.permission_classes = [IsAuthenticated]
            return super(self.__class__, self).get_permissions()

        http_method_list = permissions_from_admin_groups(user, Event.__name__)
        self.http_method_names = http_method_list

        return super(self.__class__, self).get_permissions()

    def dispatch(self, *args, **kwargs):
        """Use dispatch to update http_method_names"""
        response = super(EventViewset, self).dispatch(*args, **kwargs)
        response['Allow'] = ', '.join(self.http_method_names)
        return response

    def get_queryset(self):
        return Event.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            # pagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({"success": True, "data": serializer.data})

            serializer = self.action_serializers["create"](queryset, many=True)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                response = self.perform_create(serializer)
                return response
            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)
        errors = serializer.errors
        errors["success"] = False
        logger.error(f"error = {serializer.errors}")
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = self.request.user
        event = serializer.save()

        data = {"success": True,
                "event_id": str(event.event_id)}
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            try:
                return self.perform_update(serializer)
            except Exception as e:
                logger.error(f"request = {self.request}")
                logger.error(f"error = {e}")
                return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

        errors = serializer.errors
        errors["success"] = False
        logger.error(f"error = {serializer.errors}")
        return Response(errors, status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = serializer.save()
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        try:
            ob = self.get_object()
            ob.delete()
            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"error = {e}")
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
