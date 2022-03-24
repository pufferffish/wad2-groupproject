from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django_resized import ResizedImageField
import string

import time
import random

def random_string():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    random_string.capitalize()
    #t = time.time() - 1645000000
    #return (t << 8) | random.randint(0, 255)
    return random_string

def random_username():
    return f"user{str(random())}"

class UserInfo(models.Model):
    NICKNAME_MAX_LENGTH = 32
    # The underlying django user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The name which is shown on the website, since user.username is the microsoft email
    nickname = models.CharField(max_length=NICKNAME_MAX_LENGTH, default="")
    # The amount of tokens / money the user have
    tokens = models.PositiveIntegerField(default = 0)
    # The profile picture
    pfp = ResizedImageField(size=[500,500], upload_to='profile_images/', blank=True)

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
        verbose_name_plural = 'Categories'

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
    createdAt = models.DateTimeField(null=True)
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
        verbose_name_plural = 'PictureVotes'


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
        return f"{str(self.owner)}: {str(self.text)}"
