from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from accounts.models import User
from accounts.serializers import UserSerializer

from clients.models import Client
from clients.serializers import ClientSerializer, ClientDetailSerializer

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework import mixins, viewsets


class UserViewset(ModelViewSet):
    """ Comments list"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'user_id'  # Use to show detail page

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


class ClientViewset(ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'client_id'  # Use to show detail page

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
        data = {"success": True,
                "client_id": str(client.client_id)}
        return Response(data, status=status.HTTP_200_OK)