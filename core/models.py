from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid





User = get_user_model()
# Create your models here.

#model to store the profile info
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True)
    firstname=models.CharField(max_length=15,null=True)
    lastname=models.CharField(max_length=15,null=True)
    mobileNumber=models.BigIntegerField(null=True)
    email=models.CharField(max_length=15,null=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    
#model to store the post info
class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='posts')
    caption=models.TextField()
    posted_at=models.DateTimeField(default=datetime.now)
    no_likes=models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.user.user}'

#follower model

class Follower(models.Model):
    current_user=models.ForeignKey('Profile',blank=True,on_delete=models.CASCADE,null=True)
    following_user_id=models.ManyToManyField('Profile',blank=True,related_name='following')
    follower_user_id=models.ManyToManyField('Profile',blank=True,related_name='followers')

    def __str__(self):
        return f'{self.current_user.user}'
