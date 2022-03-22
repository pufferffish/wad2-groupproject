from django.contrib import admin
from django.urls import path, include
from OnlyPics import views

app_name = "onlypics"

urlpatterns = [
    path("", views.index, name="index"),
    path("whoami", views.whoami, name="whoami"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("logout", views.logout_user, name="logout"),
    path("about", views.about, name='about'),
    path("home", views.index, name=''),
    path("post_for_sale", views.post_for_sale, name='post_for_sale'),
    path("profile", views.profile, name='profile'),
    path("add_tokens", views.add_tokens, name='add_tokens'),
    path("explore", views.explore, name='explore'),
    path("upload", views.upload, name='upload')
]
