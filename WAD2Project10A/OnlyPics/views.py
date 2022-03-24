from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from OnlyPics.models import UserInfo, Picture, Category
from OnlyPics.forms import UserInfoForm, UpdateUserInfoForm, PostForSaleForm
from OnlyPics.hcaptcha import verify_hcaptcha_request
import numpy as np

#to be used in the template
def get_comments_according_to_picture(picture):
    comments = Comment.objects.filter(picture=picture)
    return comments

def redirect_to_index(request):
    return redirect('onlypics:index')

def getMostPopularCategories():
    categories = Category.objects.all()
    dictionary = {}
    for category in categories:
        dictionary[category.name] = len(Picture.objects.filter(tags=category))

    sortedDict = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
    topThreeCategories = list(sortedDict.keys())[:3]

    return topThreeCategories

def index(request):
    pictures = Picture.objects.all()
    context_dic = {}
    context_dic['pics'] = pictures
    context_dic['topCats'] = getMostPopularCategories()
    return render(request, 'onlypics/index.html', context=context_dic)

def explore(request):
    picture_list = Picture.objects.all()
    categories = Category.objects.all()
    context_dic = {}
    context_dic['pictures'] = picture_list
    context_dic['categories'] = categories
    context_dic['topCats'] = getMostPopularCategories()

    return render(request, 'onlypics/explore.html', context=context_dic)

def about(request):
    context_dic = {}
    context_dic['topCats'] = getMostPopularCategories()
    return render(request, 'onlypics/about.html', context=context_dic)

@login_required
def post_for_sale(request):
    form = PostForSaleForm()
    if request.method == 'POST':
        form = PostForSaleForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('onlypics:index')
        else:
            print(form.errors)

    return render(request, 'onlypics/post_for_sale.html', {'form':form})

@login_required
def profile(request):
    user = UserInfo.objects.get(user = request.user)
    pictures = Picture.objects.filter(owner = user)
    context_dic = {}
    context_dic['pictures'] = pictures
    return render(request, 'onlypics/profile.html', context=context_dic)

# calculate how many tokens should be gained
# in add_tokens.html
def calculate_tokens_gain(user):
    return 50

@login_required
def add_tokens(request):
    topCategories = getMostPopularCategories()
    INVALID_CAPTCHA_REASON = "invalidCaptcha"
    user = UserInfo.objects.get(user=request.user)
    if request.method == 'POST':
        try:
            verify_hcaptcha_request(request)
            user.tokens += calculate_tokens_gain(request)
            user.save()
            return redirect('onlypics:add_tokens')
        except CaptchaException:
            return redirect(reverse('onlypics:add_tokens') + "?error=" + INVALID_CAPTCHA_REASON)
        except Exception:
            return redirect(reverse('onlypics:add_tokens') + "?error=unknown")
    else:
        gain = calculate_tokens_gain(user)
        current_tokens = user.tokens
        error_reason = request.GET.get("error", None)
        if error_reason == None:
            error_message = ""
        elif error_reason == INVALID_CAPTCHA_REASON:
            error_message = "Invalid hCaptcha, Please try again."
        else:
            error_message = "Unknown error. Please try again."
        return render(request, 'onlypics/add_tokens.html', {"gain":  gain, 'current_tokens': current_tokens, 'error_msg': error_message, 'topCats':topCategories})

# testing purpose
def whoami(request):
    if not request.user.is_authenticated:
        return HttpResponse(f"You are not logged in")
    user = request.user
    try:
        user_info = UserInfo.objects.get_or_create(user=user, tokens=50)[0]
        return HttpResponse(f"You are {user_info.nickname}")
    except UserInfo.DoesNotExist:
        return HttpResponse("You are logged in but there's no profile of you")

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
    disallowed_characters = "._! ,/[]()"

    if 'search' in request.GET:
        search_term = request.GET['search']

    for character in disallowed_characters:
        search_term = search_term.replace(character, "")

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
    target = [k for k in token1]
    source = [k for k in token2]

    distances = np.zeros((len(source), len(target)))

    distances[0] = [j for j in range(len(target))]
    distances[:,0] = [j for j in range(len(source))]

    for column in range(1, len(target)):
        for row in range(1, len(source)):
            if (target[column] != source[row]):
                distances[row][column] = min(distances[row-1][column], distances[row][column-1]) + 1
            else:
                distances[row][column] = distances[row - 1][column-1]

    return distances[len(source) - 1][len(target) - 1]
def calcDictDistance(word):
    pictures = Picture.objects.all()
    disallowed_characters = "._! ,/[]()"

    dictWordDist = {}
    wordIdx = 0

    for pic in pictures:
        splitPicName = pic.name
        for character in disallowed_characters:
            splitPicName = splitPicName.replace(character,"")

        wordDistance = levenshteinDistanceDP(word, splitPicName)

        if wordDistance >= 10:
            wordDistance = 9
        dictWordDist[wordDistance] = pic
        wordIdx = wordIdx + 1

    sortedDict = dict(sorted(dictWordDist.items(), key=lambda x: x[0]))

    return sortedDict.values()

def account(request):
    user = request.user
    user_info = UserInfo.objects.get(user=user)

    pictures = Picture.objects.filter(owner=user_info)
    len_of_pictures = len(pictures)

    context_dic = {}
    context_dic['pictures'] = pictures
    context_dic['userInfo'] = user_info
    context_dic['len_pics'] = len_of_pictures
    context_dic['topCats'] = getMostPopularCategories()

    return render(request, 'onlypics/account.html', context=context_dic)

@login_required
def edit_account(request):
    userInfoForm = UpdateUserInfoForm()

    if request.method == 'POST':
        userInfoForm = UpdateUserInfoForm(request.POST, request.FILES, instance=request.user.userinfo)
        if userInfoForm.is_valid():
            info = userInfoForm.save(commit=False)
            info.user = request.user
            info.save()
            return redirect('onlypics:index')
        else:
            print(form.errors)

    return render(request, 'onlypics/edit_account.html', {'form':userInfoForm})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('onlypics:index')

    return render(request, 'onlypics/delete_account.html')