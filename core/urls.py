from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from core.views import *

router_user = routers.DefaultRouter()
router_user.register('user', UserViewSet, basename='user')
router_user.register('search', UserSearchViewSet, basename='search')
router_user.register('friendship', FriendshipViewSet, basename='friendship')


urlpatterns = [
    path('', include(router_user.urls)), 
]
