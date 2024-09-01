from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True,blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
   
    def __str__(self):
        return "{}".format(self.email)
    

class Friendship(models.Model):
    requested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requested_user')    
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')   
    is_request_accept = models.BooleanField(default=False) 
    is_request_ignore = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
