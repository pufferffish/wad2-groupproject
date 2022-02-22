from django.contrib import admin
from django.urls import path, include
from OnlyPics import views

app_name = "onlypics"

urlpatterns = [
    path("", views.index, name="index"),
    path("whoami", views.whoami, name="whoami")
]
