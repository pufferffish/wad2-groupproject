from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from OnlyPics.models import UserInfo, Picture, Category
from OnlyPics.forms import UserInfoForm
from OnlyPics.hcaptcha import verify_hcaptcha_request
import numpy as np

#to be used in the template
def get_comments_according_to_picture(picture):
    comments = Comment.objects.filter(picture=picture)
    return comments

def redirect_to_index(request):
    return redirect('onlypics:index')

def index(request):
    top_five_most_liked_pictures = Picture.objects.all()
    context_dic = {}
    context_dic['pics'] = top_five_most_liked_pictures
    return render(request, 'onlypics/index.html', context=context_dic)

def explore(request):
    picture_list = Picture.objects.all()
    categories = Category.objects.all()
    context_dic = {}
    context_dic['pictures'] = picture_list
    context_dic['categories'] = categories

    return render(request, 'onlypics/explore.html', context=context_dic)

def about(request):
    return render(request, 'onlypics/about.html')

@login_required
def post_for_sale(request):
    return HttpResponse("Not yet implemented!")
    #form = PostForSaleForm()
    #if request.method == 'POST':
        #form = PostForSaleForm(request.POST)
        #if form.is_valid():
            #form.save(commit=True)
            #return redirect('onlypics:index')
        #else
            #print(form.errors)

     #return render(request, 'onlypics/post_for_sale.html', {'form':form})

@login_required
def profile(request):
    user = request.user
    pictures = Picture.objects.filter(user = user)


@login_required
def add_tokens(request):
    return HttpResponse("Not yet implemented!")

def whoami(request):
    if not request.user.is_authenticated:
        return HttpResponse(f"You are not logged in")
    user = request.user
    try:
        user_info = UserInfo.objects.get_or_create(user=user, tokens=50)[0]
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

@login_required
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('onlypics:index')

@login_required
def upload(request):
    form = UserInfoForm()
    user = request.user
    try:
        user_info = UserInfo.objects.get(user=user)
    except UserInfo.DoesNotExist:
        if request.method == 'POST':
            form = UserInfoForm(request.POST, request.FILES)
            if form.is_valid():
                if user:
                    user_info = form.save(commit=False)
                    user_info.user = user
                    user_info.save()

                    return redirect('onlypics:index')
            else:
                print(form.errors)
    else:
        return redirect('onlypics:index')
    return render(request, 'onlypics/upload.html', {'form':form})

@login_required
def search(request):
    categories = Category.objects.all()

    if 'search' in request.GET:
        search_term = request.GET['search']

    if (len(search_term) == 0):
        context_dic_empty = {}
        picture_list = Picture.objects.all()

        context_dic_empty['pictures'] = picture_list
        context_dic_empty['categories'] = categories

        return render(request, 'onlypics/explore.html', context=context_dic_empty)

    picture_list = calcDictDistance(search_term)
    context_dic = {}
    context_dic['pictures'] = picture_list
    context_dic['categories'] = categories

    return render(request, 'onlypics/explore.html', context=context_dic)


def levenshteinDistanceDP(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1 - 1] == token2[t2 - 1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]
def calcDictDistance(word):
    pictures = Picture.objects.all()

    dictWordDist = {}
    wordIdx = 0

    for pic in pictures:
        wordDistance = levenshteinDistanceDP(word, pic.name)

        if wordDistance >= 10:
            wordDistance = 9
        dictWordDist[wordDistance] = pic
        wordIdx = wordIdx + 1

    closestWordsSorted = []
    wordDetails = []
    currWordDist = 0
    sortedDict = dict(sorted(dictWordDist.items(), key=lambda x: x[0]))

    return sortedDict.values()