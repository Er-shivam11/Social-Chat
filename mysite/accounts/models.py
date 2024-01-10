from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class UserType(models.Model):
    type_name = models.CharField(verbose_name="Type Name", max_length=150, unique=True,null=True, blank=True)
    is_active = models.BooleanField(blank=False,null=True)

    class Meta:
        db_table = 'tbl_username'
        verbose_name = 'User Type'
        verbose_name_plural = 'Users Type'
    
    def __str__(self) -> str:
        return self.type_name


class CustomUser(User):        
    age = models.PositiveIntegerField(null=True, blank=True)
    user_type = models.ForeignKey(
        UserType, verbose_name='User Type', on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    interests = models.CharField(max_length=255, blank=True)
    twitter_profile = models.URLField(blank=True)
    instagram_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
    created_at = models.DateTimeField(
        verbose_name='Created At', auto_now_add=True, null=True, blank=False)
    updated_at = models.DateTimeField(
        verbose_name='Updated At', auto_now=True, null=True, blank=False)

    # Specify unique related_name values to avoid clashes
    

    class Meta:
        db_table = 'tbl_profile'

    def __str__(self):
        return self.username

class UserRelationship(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following_relationships')
    followed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower_relationships')

    class Meta:
        db_table = 'tbl_followers'

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"

