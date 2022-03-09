from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django_resized import ResizedImageField

import time
import random

def random():
    t = time.time() - 1645000000
    return (t << 8) | random.randint(0, 255)

def random_username():
    return f"user{str(random())}"

class UserInfo(models.Model):
    # The underlying django user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The name which is shown on the website, since user.username is the microsoft email
    nickname = models.CharField(max_length=32, default=random_username)
    # The amount of tokens / money the user have
    tokens = models.PositiveIntegerField(default = 0)
    # The profile picture
    pfp = ResizedImageField(size=[500,500], force_format='JPG', upload_to='profile_images')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user'),
            models.UniqueConstraint(fields=['nickname'], name='unique_nickname'),
        ]

    def __str__(self):
        return self.nickname

class Category(models.Model):
    # name of the category
    name = models.CharField(max_length=255)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_name'),
        ]

    def __str__(self):
        return self.name

class Picture(models.Model):
    # The owner of the picture
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    # The amount of tokens / money to buy the picture
    # Use negative number to denote as not for sale
    price = models.IntegerField(default = -1)
    # The name of the picture
    name = models.CharField(max_length=100)
    # The tags / categories which the picture belong to
    # Store the tags in such format: 'tag1;tag2;tag3;'
    # It's a workaround since django with sqlite doesn't support storing array
    tags = models.ForeignKey(Category, on_delete=models.CASCADE)
    # when the picture was first created
    createdAt = models.DateTimeField()
    # The uploaded picture
    upload = models.ImageField(upload_to ='uploads/')

    def __str__(self):
        return self.name

class PictureVotes(models.Model):
    # The user who casted the vote
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    # The picture which the vote is casted on
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    # Whether the vote is positive (a like) or negative (a dislike)
    positive = models.BooleanField()

    class Meta:
        unique_together = [ 'user', 'picture' ]

class Comment(models.Model):
    # The user who made the comment
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    # The picture which the comment is made on
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    # The content of the comment
    text = models.TextField()
    # The time when the comment is made
    made_at = models.DateTimeField()

    def __str__(self):
        f"{str(self.owner)}: {str(self.text)}"
