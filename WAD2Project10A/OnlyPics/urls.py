from django.contrib import admin
from django.urls import path, include
from OnlyPics import views

app_name = "onlypics"

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_user, name="logout"),
    path("about", views.about, name='about'),
    path("home", views.index, name=''),
    path("post_for_sale", views.post_for_sale, name='post_for_sale'),
    path("profile", views.profile, name='profile'),
    path("add_tokens", views.add_tokens, name='add_tokens'),
    path("explore", views.explore, name='explore'),
    path("upload", views.upload, name='upload'),
    path("search", views.search, name='search'),

    path("account", views.account, name='account'),
    path("edit_account", views.edit_account, name='edit_account'),
    path("delete_account", views.delete_account, name='delete_account'),

    path("post_comment", views.post_comment, name='post_comment'),
    path("like_picture", views.like_picture, name='like_picture'),
]
