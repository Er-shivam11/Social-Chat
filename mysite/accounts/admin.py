from django.contrib import admin
from .models import UserType,CustomUser,UserRelationship

# Register your models here.
admin.site.register(UserType)
admin.site.register(CustomUser)
admin.site.register(UserRelationship)