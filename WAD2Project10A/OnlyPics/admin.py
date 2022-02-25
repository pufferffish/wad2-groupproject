from django.contrib import admin

from django.contrib import admin
from OnlyPics.models import UserInfo, Picture, PictureVotes, Comment, Category

admin.site.register(UserInfo)
admin.site.register(Category)
admin.site.register(Picture)
admin.site.register(Comment)
admin.site.register(PictureVotes)
