from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from OnlyPics.models import UserInfo
from OnlyPics.hcaptcha import verify_hcaptcha_request

def index(request):
    return render(request, 'onlypics/index.html')

def about(request):
    return render(request, 'onlypics/about.html')

def explore(request):
    return render(request, 'onlypics/explore.html')

def whoami(request):
    if not request.user.is_authenticated:
        return HttpResponse(f"You are not logged in")
    user = request.user
    try:
        user_info = UserInfo.objects.get(user = user)
        return HttpResponse(f"You are {user_info.nickname}")
    except UserInfo.DoesNotExist:
        return HttpResponse("You are logged in but there's no profile of you")

# hCaptcha testing
def vbucks(request):
    if request.method == 'POST':
        verify_hcaptcha_request(request)
        return HttpResponse("let it out")
    else:
        return render(request, 'onlypics/vbucks.html')

@login_required
def edit_profile(request):
    return HttpResponse("Joke")

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("You have logged out.")
    else:
        return HttpResponse("You have already logged out.")
