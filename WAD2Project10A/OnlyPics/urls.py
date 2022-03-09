from django.contrib import admin
from django.urls import path, include
from OnlyPics import views

app_name = "onlypics"

urlpatterns = [
    path("", views.index, name="index"),
    path("whoami", views.whoami, name="whoami"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("logout", views.logout_user, name="logout"),
    path("vbucks", views.vbucks, name="vbucks"),
    path("base", views.base, name='base'),
]
