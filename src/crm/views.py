from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .models import Client
from .serializers import ClientSerializer
from rest_framework.response import Response
from rest_framework import status

