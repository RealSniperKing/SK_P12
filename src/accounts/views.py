from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer


class UsersViewset(ModelViewSet):
    """ Comments list"""
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    # lookup_field = 'comment_id'  # Use to show detail page
    #
    def get_queryset(self):
        return User.objects.all()