from core.models import *
from core.serializers import *
from master.constants import SUCCESS_RESPONSE, FAILURE_RESPONSE, RESPONSE, SIMPLE_RESPONSE
from master.messages import RESPONSE_MESSAGE
from django.core.validators import validate_email
from rest_framework import status
from core.utils import fetch_user_by_email
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

def user_signup(username,password,email,full_name):
    """
    This fn creates user 
    :param email:
    :param fullname:
    :param username:
    :return:
    """
    try:
        validate_email(email)
    except:
        RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['INVALID_EMAIL']
        RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
        return RESPONSE, 400
    if User.objects.filter(username=username).exists():
        RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['USERNAME_ALREADY_PRESENT']
        RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
        return RESPONSE, 400
    if User.objects.filter(email=email).exists():
        RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['EMAIL_ALREADY_PRESENT']
        RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
        return RESPONSE, 400
    else:
        _user = User(full_name=full_name,email=email,username=username,is_active=True)
        _user.set_password(password)
        _user.save()
        RESPONSE['message'] = RESPONSE_MESSAGE['SUCCESS']['SIGN_UP']
        RESPONSE['ResponseCode'] = status.HTTP_200_OK
        return RESPONSE, 200
    
def user_login(email,password):
    try:
        validate_email(email)
    except:
        RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['INVALID_EMAIL']
        RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
        return RESPONSE, 400
    if User.objects.filter(email=email).exists():
        a = User.objects.get(email=email)
        if a.is_active:
            _data = fetch_user_by_email(email, password)
            return _data, 200 
        else:
            RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['USER_NOT_ACTIVE']
            RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
            return RESPONSE, 400  
    else:
        RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['USER_NOT_FOUND']
        RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
        return RESPONSE, 400
    
def user_search(search=None):
    # If search is None or empty, return all users
    if not search:
        users = User.objects.filter(is_active=True)
    else:
        exact_email_match = User.objects.filter(email__iexact=search)

        if exact_email_match.exists():
            users = exact_email_match
        else:
            users = User.objects.filter(full_name__icontains=search)

    paginator = Paginator(users, 10)
    page = paginator.get_page(1) 
    data = UserSerializer(page, many=True).data
    response = {
        "message": "Success",
        "data": data,
        "total_results": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": page.number,
    }
    return response, status.HTTP_200_OK

def friendship_request_user(user,request_to_user_id):
    if not User.objects.filter(id=request_to_user_id).exists():
        RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['TO_USER_NOT_FOUND']
        RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
        return RESPONSE, 400
    if Friendship.objects.filter(Q(requested_user=user,to_user=request_to_user_id) | Q(requested_user=request_to_user_id,to_user=user)).exists():
        RESPONSE['message'] = RESPONSE_MESSAGE['SUCCESS']['FRIEND_REQUEST_SENT_ALREADY']
        RESPONSE['ResponseCode'] = status.HTTP_200_OK
        return RESPONSE, 200
    else:
        # Check the number of requests sent by the user within the last minute
        one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
        recent_requests = Friendship.objects.filter(
            requested_user=user,
            created_at__gte=one_minute_ago
        ).count()

        if recent_requests >= 3:
            RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['SEND_REQUEST_LIMIT_REACHED']
            RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
            return RESPONSE, 400
        
        frend = Friendship(requested_user=user,to_user=User.objects.get(id=request_to_user_id))
        frend.save()
        RESPONSE['message'] = RESPONSE_MESSAGE['SUCCESS']['FRIEND_REQUEST_SENT']
        RESPONSE['ResponseCode'] = status.HTTP_200_OK
        return RESPONSE, 200
    
def friendship_request_accept_reject(user,to_user_id,rstatus,is_ignore):
    if Friendship.objects.filter(to_user=user,requested_user=to_user_id).exists():
        frnd = Friendship.objects.filter(to_user=user,requested_user=to_user_id)
        req_status = True if rstatus == "true" else False
        req_ignore = True if is_ignore == "true" else False
        frnd.update(is_request_accept=req_status,is_request_ignore=req_ignore)
        if req_ignore:
            RESPONSE['message'] = RESPONSE_MESSAGE['SUCCESS']['SUCCESS']
        if req_status: 
            RESPONSE['message'] = RESPONSE_MESSAGE['SUCCESS']['FRIEND_REQUEST_ACCEPT']
        else:
            RESPONSE['message'] = RESPONSE_MESSAGE['SUCCESS']['FRIEND_REQUEST_REJECT']
        RESPONSE['ResponseCode'] = status.HTTP_200_OK
        return RESPONSE, 200 
    RESPONSE['message'] = RESPONSE_MESSAGE['FAILURE']['NO_DATA']
    RESPONSE['ResponseCode'] = status.HTTP_400_BAD_REQUEST
    return RESPONSE, 400
    
def friendship_received_request_list(user):
    receive_req_list = Friendship.objects.filter(to_user=user,is_request_accept=False)
    serializer = FriendshipSerializer(receive_req_list, many=True)
    SUCCESS_RESPONSE['message'] = RESPONSE_MESSAGE['SUCCESS']['SUCCESS']
    SUCCESS_RESPONSE['data'] = serializer.data
    SUCCESS_RESPONSE['ResponseCode'] = status.HTTP_200_OK
    return SUCCESS_RESPONSE, 200

def get_friend_list(user):
    friends_list = Friendship.objects.filter((Q(requested_user=user) | Q(to_user=user)) & Q(is_request_accept=True))
    serializer = FriendshipSerializer(friends_list, many=True)
    SUCCESS_RESPONSE['message'] = RESPONSE_MESSAGE['SUCCESS']['SUCCESS']
    SUCCESS_RESPONSE['data'] = serializer.data
    SUCCESS_RESPONSE['ResponseCode'] = status.HTTP_200_OK
    return SUCCESS_RESPONSE, 200    