from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout

from django.core import serializers
from django.http import JsonResponse

from OnlyPics.models import UserInfo, Picture, Category, PictureVotes, Comment
from OnlyPics.forms import UserInfoForm, UpdateUserInfoForm, PostForSaleForm, PostCommentForm

from OnlyPics.hcaptcha import CaptchaException, verify_hcaptcha_request

from datetime import datetime
import numpy as np
import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

INVALID_CAPTCHA_REASON = "invalidCaptcha"
INVALID_PICTURE_REASON = "invalidPicture"

def resolve_error_message(error_reason):
    if error_reason == None:
        return ""
    elif error_reason == INVALID_CAPTCHA_REASON:
        return "Invalid hCaptcha. Please try again."
    elif error_reason == INVALID_PICTURE_REASON:
        return "You have uploaded an invalid picture. Please try again."
    else:
        return "Unknown error. Please try again."

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
    filter_query = request.GET.get("filter", None)
    try:
        filter_category = Category.objects.get(name = filter_query)
        picture_list = Picture.objects.filter(tags = filter_category)
    except:
        picture_list = Picture.objects.all()
    categories = Category.objects.all()
    comments = Comment.objects.all()
    
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=request.user)
        context_dic['user_info'] = user_info

    form = PostCommentForm()
    context_dic['pictures'] = picture_list
    context_dic['categories'] = categories
    context_dic['topCats'] = getMostPopularCategories()
    context_dic['comments'] = comments
    context_dic['form'] = form

    return render(request, 'onlypics/explore.html', context=context_dic)

def about(request):
    context_dic = {}
    context_dic['topCats'] = getMostPopularCategories()
    return render(request, 'onlypics/about.html', context=context_dic)

# convert to jpeg and ensure file is a picture
def image_reformat(image):
    img_io = io.BytesIO()
    img = Image.open(image)
    img.save(img_io, format="PNG")
    new_pic = InMemoryUploadedFile(img_io, 'ImageField', image.name, 'JPEG', sys.getsizeof(img_io), None)
    return new_pic

@login_required
def post_for_sale(request):
    if request.method == 'POST':
        try:
            user = UserInfo.objects.get(user=request.user)
            query = request.POST
            picture = Picture()
            picture.owner = user
            if query['forSale'] == 'on':
                picture.price = int(query['price'])
            else:
                picture.price = -1
            picture.tags = Category.objects.get(name=query['category'])
            picture.createdAt = query['createdAt']
            picture.name = query['name']
            image = request.FILES['upload']
            image = image_reformat(image)
            picture.upload.save(image.name, image)
            picture.save()
            return redirect('onlypics:account')
        except Exception as e:
            print(e)
            return redirect(request.build_absolute_uri() + "?error=" + INVALID_PICTURE_REASON)

    context_dic = {}
    context_dic["categories"] = Category.objects.all()
    context_dic["error_message"] = resolve_error_message(request.GET.get("error", None))
    return render(request, 'onlypics/post_for_sale.html', context_dic)

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
        error_message = resolve_error_message(request.GET.get("error", None))
        context_dic = {"gain":  gain, 'current_tokens': current_tokens, 'error_msg': error_message, 'topCats': topCategories}
        return render(request, 'onlypics/add_tokens.html', context_dic)

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

def search(request):
    search_term = ""
    if request.user.is_authenticated:
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
    else:
        redirect('onlypics:explore')

def levenshteinDistanceDP(token1, token2):
    if token1 == "":
        return len(token2)
    if token2 == "":
        return len(token1)

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
    pictureVotes = PictureVotes.objects.all()
    positiveVotes = {}
    negativeVotes = {}

    for pic in pictures:
        positiveVotes[pic] = len(PictureVotes.objects.filter(picture = pic, positive = True))
        negativeVotes[pic] = len(PictureVotes.objects.filter(picture = pic, positive = False))

    len_of_pictures = len(pictures)

    context_dic = {}
    context_dic['pictures'] = pictures
    context_dic['userInfo'] = user_info
    context_dic['len_pics'] = len_of_pictures
    context_dic['topCats'] = getMostPopularCategories()
    context_dic['positiveVotes'] = positiveVotes
    context_dic['negativeVotes'] = negativeVotes

    return render(request, 'onlypics/account.html', context=context_dic)

@login_required
def edit_account(request):
    userInfoForm = UpdateUserInfoForm()

    if request.method == 'POST':
        try:
            userInfoForm = UpdateUserInfoForm(request.POST, request.FILES, instance=request.user.userinfo)
            assert userInfoForm.is_valid()
            info = userInfoForm.save(commit=False)
            info.user = request.user
            info.save()
            return redirect('onlypics:account')
        except:
            return redirect(request.build_absolute_uri() + "?error=" + INVALID_PICTURE_REASON)

    error_message = resolve_error_message(request.GET.get("error", None))
    return render(request, 'onlypics/edit_account.html', context={'form': userInfoForm, 'error_message': error_message})

@login_required
def upload(request):
    form = UserInfoForm()
    user = request.user
    try:
        user_info = UserInfo.objects.get(user=user)
        return redirect('onlypics:index')
    except UserInfo.DoesNotExist:
        if request.method == 'POST':
            try:
                form = UserInfoForm(request.POST, request.FILES)
                assert form.is_valid()
                assert user
                user_info = form.save(commit=False)
                user_info.user = user
                user_info.save()
                return redirect('onlypics:index')
            except:
                return redirect(request.build_absolute_uri() + "?error=" + INVALID_PICTURE_REASON)
    error_message = resolve_error_message(request.GET.get("error", None))
    return render(request, 'onlypics/upload.html', context={'form': form, 'error_message': error_message})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('onlypics:index')

    return render(request, 'onlypics/delete_account.html')

@login_required
def post_comment(request):
    if request.method == 'POST' and request.is_ajax:
        try:
            data = request.POST
            uuid = data['picture_uuid']
            instance = Comment()
            instance.owner = UserInfo.objects.get(user=request.user)
            instance.text = data['text']
            instance.picture = Picture.objects.get(id=uuid)
            instance.made_at = datetime.now()
            instance.save()

            return JsonResponse({"nickname": instance.owner.nickname, "text": instance.text, "uuid": uuid}, status=200)
        except:
            return JsonResponse({'error': form.errors}, status=400)

    return JsonResponse({"error": ""}, status=400)

@login_required
def like_picture(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.is_ajax:
            try:
                data = request.POST
                uuid = data['picture_uuid']
                user_info = UserInfo.objects.get(user=request.user)
                picture = Picture.objects.get(id=uuid)

                instance = PictureVotes()
                instance.user = user_info
                instance.picture = picture
                if data.get("likeButton"):
                    instance.positive = True
                elif data.get("dislikeButton"):
                    instance.positive = False

                like_result = instance.positive
                instance.save()

                return JsonResponse({"like_result": like_result, "uuid": uuid}, status=200)
            except:
                error_message = "You have already "
                existing_like_result = PictureVotes.objects.get(user=user_info, picture=picture)
                return JsonResponse({"error": error_message, "like_result": existing_like_result.positive, "uuid": uuid}, status=200)
        return JsonResponse({"error": ""}, status=400)

@login_required
def buy_picture(request):
    if request.method == 'GET' and request.is_ajax:
        picture_id = request.GET.get('picture_id')
        user = UserInfo.objects.get(user=request.user)
        picture = Picture.objects.get(id=picture_id)

        if user.tokens > picture.price and picture.price != -1:
            user.tokens -= picture.price
            picture.owner = user
            picture.price = -1

            user.save()
            picture.save()
            return redirect('onlypics:account')
        else:
            return JsonResponse({'result':'failure'}, status=200)

    return JsonResponse({"error": ""}, status=400)





def terms_and_conditions(request):
    context_dic = {}
    context_dic['topCats'] = getMostPopularCategories()
    return render(request, 'onlypics/tos.html', context=context_dic)

