from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.serializers import CustomTokenObtainPairSerializer
from django.contrib.auth import authenticate
from core.models import User
from master.constants import USER_DETAILS_RESPONSE,FAILURE_RESPONSE, RESPONSE
from master.messages import RESPONSE_MESSAGE
from rest_framework import status
import datetime

def fetch_user_by_email(email,password):
    """
    Fn to fetch user data
    :param email:
    :param password:
    :return:
    """
    user = authenticate(email=email, password=password)
    if user.is_active:   
        tokenr = CustomTokenObtainPairSerializer(TokenObtainPairSerializer).get_token(user)
        tokena = str(tokenr.access_token)

        user_data = User.objects.filter(email=email).values()[0]
        user_data_response = {str(key): value for key, value in user_data.items() if key != 'password' and not isinstance(key, datetime.datetime)}
        SUCCESS_RESPONSE = {
            'data': {
                'refresh': str(tokenr),
                'access': tokena,
                'user_id': user.id,
                **user_data_response,
                'active_status': user_data_response.get('is_active', False),
            },
            'message': "User Login successfully",
            'ResponseCode': status.HTTP_200_OK
        }
        return SUCCESS_RESPONSE
    else:
        RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['USER_NOT_ACTIVE']
        RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
        return RESPONSE 
