from django.contrib import admin
from core.models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','username','full_name')

admin.site.register(User,UserAdmin)

class FriendshipAdmin(admin.ModelAdmin):
    list_display =['requested_user','to_user','is_request_accept','request_sent_at']
    readonly_fields = ['requested_user','to_user']
    def request_sent_at(self, obj):
        return obj.created_at
admin.site.register(Friendship,FriendshipAdmin)