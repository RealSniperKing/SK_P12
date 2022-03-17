"""EpicEvents URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from rest_framework import routers
from .views import ClientViewset, ContractViewset, EventViewset, error500, SigninViewset, UserViewset, SignoutViewset
from django.conf import settings
from django.conf.urls import handler404

# handler404 = error404

# Create router
router = routers.SimpleRouter()
router.register('signin', SigninViewset, basename='signin')
router.register('users', UserViewset, basename='users')
router.register('clients', ClientViewset, basename='clients')
router.register('contracts', ContractViewset, basename='contracts')
router.register('events', EventViewset, basename='events')

app_name = "api"
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/signout', SignoutViewset.as_view(), name='signout'),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    print("ddd")
    urlpatterns.append(path('500/', error500, name='500'))
