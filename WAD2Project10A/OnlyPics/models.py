from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class UserInfo(models.Model):
    # The underlying django user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The amount of tokens / money the user have
    tokens = models.PositiveIntegerField(default = 0)
    # The profile picture
    pfp = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

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
    tags = models.CharField(max_length=256)
    # upvotes / downvotes (likes / dislikes)
    upvote = models.PositiveIntegerField(default = 0)
    downvote = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.name
