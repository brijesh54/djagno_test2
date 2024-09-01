from django.shortcuts import render
from core.models import *
from core.serializers import *
from rest_framework import viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_200_OK
from master.constants import FAILURE_RESPONSE, SUCCESS_RESPONSE, RESPONSE,SIMPLE_RESPONSE
from master.messages import RESPONSE_MESSAGE
from core.controller import *
# Create your views here.

class UserViewSet(viewsets.GenericViewSet):
    """
    View set for user
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['POST'], url_name='register', url_path='register')
    def sign_up(self, request):
        """
        API to handle user sign up
        """
        try:
            message, status = user_signup(request.data['username'],
                                            request.data['password'],
                                            request.data['email'],
                                            request.data['full_name'])

            if status == 200:
                return Response(message)
            return Response(message, status=HTTP_400_BAD_REQUEST)
        except:
            FAILURE_RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['KEY_ERROR']
            return Response(FAILURE_RESPONSE, status=HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['POST'], url_name='login', url_path='login')
    def login(self, request):
        """
        API to handle user login
        """
        try:
            message, status = user_login(request.data['email'],request.data['password'])

            if status == 200:
                return Response(message)
            return Response(message, status=HTTP_400_BAD_REQUEST)
        except:
            FAILURE_RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['KEY_ERROR']
            return Response(FAILURE_RESPONSE, status=HTTP_400_BAD_REQUEST)
        
class UserSearchViewSet(viewsets.GenericViewSet):
    """
    View set for user Search
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], url_name='user_email_fullname', url_path='user_email_fullname')
    def user_search(self, request):
        """
        API to handle user search
        """
        try:
            search = request.query_params.get('search', None)
            message, status = user_search(search)

            if status == 200:
                return Response(message)
            return Response(message, status=HTTP_400_BAD_REQUEST)
        except:
            FAILURE_RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['KEY_ERROR']
            return Response(FAILURE_RESPONSE, status=HTTP_400_BAD_REQUEST)

        
class FriendshipViewSet(viewsets.GenericViewSet):
    """
    View set for Friendship
    """
    permission_classes = [IsAuthenticated]        

    @action(detail=False, methods=['POST'], url_name='send-request', url_path='send-request')
    def friendship_request_send_user(self, request):
        try:
            message, status = friendship_request_user(request.user,request.data['user_id'])
            if status == 200:
                return Response(message)
            return Response(message, status=HTTP_400_BAD_REQUEST)
        except:
            FAILURE_RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['KEY_ERROR']
            return Response(FAILURE_RESPONSE, status=HTTP_400_BAD_REQUEST)    

    @action(detail=False, methods=['POST'], url_name='request-accept-reject', url_path='request-accept-reject')
    def friendship_request_accept_reject(self, request):
        try:
            message, status = friendship_request_accept_reject(request.user,request.data['user_id'],request.data['status'],request.data['is_ignore'])
            if status == 200:
                return Response(message)
            return Response(message, status=HTTP_400_BAD_REQUEST)
        except:
            FAILURE_RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['KEY_ERROR']
            return Response(FAILURE_RESPONSE, status=HTTP_400_BAD_REQUEST)    

    @action(detail=False, methods=['GET'], url_name='recieve-request-list', url_path='recieve-request-list')
    def friendship_received_request_list(self, request):
        try:
            message, status = friendship_received_request_list(request.user)
            if status == 200:
                return Response(message)
            return Response(message, status=HTTP_400_BAD_REQUEST)
        except:
            FAILURE_RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['KEY_ERROR']
            return Response(FAILURE_RESPONSE, status=HTTP_400_BAD_REQUEST)       

    @action(detail=False, methods=['GET'], url_name='friend-list', url_path='friend-list')
    def get_myfriend_list(self, request):
        try:
            message, status = get_friend_list(request.user)
            if status == 200:
                return Response(message)
            return Response(message, status=HTTP_400_BAD_REQUEST)
        except:
            FAILURE_RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['KEY_ERROR']
            return Response(FAILURE_RESPONSE, status=HTTP_400_BAD_REQUEST)    
