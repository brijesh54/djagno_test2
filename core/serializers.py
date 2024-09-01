from core.models import *
from core.serializers import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from master.messages import RESPONSE_MESSAGE
from master.constants import USER_DETAILS_RESPONSE,FAILURE_RESPONSE
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','username','full_name','is_active')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    FAILURE_RESPONSE['message'] = "No active account found with the given credentials"
    FAILURE_RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
    default_error_messages = {
        'no_active_account': FAILURE_RESPONSE
    }   
    def validate(self, attrs):
        data = super().validate(attrs)
        return data      
    
class FriendshipSerializer(serializers.ModelSerializer):
    requested_user_username = serializers.CharField(source='requested_user.username', read_only=True)
    to_user_username = serializers.CharField(source='to_user.username', read_only=True)

    class Meta:
        model = Friendship
        fields = ('id', 'requested_user', 'to_user', 'requested_user_username', 'to_user_username', 'is_request_accept', 'is_request_ignore', 'created_at', 'updated_at')