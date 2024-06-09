from django.contrib import admin

from accounts.models import Friendship, User, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Friendship)