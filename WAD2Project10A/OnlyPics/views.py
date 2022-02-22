from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from OnlyPics.models import UserInfo

def index(request):
    return HttpResponse(
            """
            Connection terminated.
            I'm sorry to interrupt you, Elizabeth. If you still even remember that name.
            But I'm afraid you've been misinformed.
            """)

def whoami(request):
    if not request.user.is_authenticated:
        return HttpResponse(f"You are not logged in")
    user = request.user
    try:
        user_info = UserInfo.objects.get(user = user)
        return HttpResponse(f"You are {user_info.nickname}")
    except UserInfo.DoesNotExist:
        return HttpResponse("You are logged in but there's no profile of you")

@login_required
def edit_profile(request):
    return HttpResponse("Joke")

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("You have logged out.")
    else:
        return HttpResponse("You have already logged out.")
