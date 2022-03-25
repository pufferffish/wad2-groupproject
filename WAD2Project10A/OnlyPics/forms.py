from django import forms
from OnlyPics.models import UserInfo
from django.contrib.auth.models import User
from OnlyPics.models import Picture, Comment

class UserInfoForm(forms.ModelForm):
    nickname = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder':'Username',
                'class':'form-control'
            }),
        max_length = UserInfo.NICKNAME_MAX_LENGTH,
        label='Username'
    )
    tokens = forms.IntegerField(widget=forms.HiddenInput(), initial=50)

    pfp = forms.FileField(
        required=True,
        label='Profile Picture'
    )

    pfp.widget.attrs.update(
        {'class':'form-control',
         'onchange':"preview()",
         'name':'filename'})

    class Meta:
        model = UserInfo
        fields = ('nickname','pfp')

class UpdateUserInfoForm(forms.ModelForm):
    nickname = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control'
            }),
        max_length=UserInfo.NICKNAME_MAX_LENGTH,
        label='Username'
    )

    pfp = forms.FileField(
        required=True,
        label='Profile Picture'
    )

    pfp.widget.attrs.update(
        {'class': 'form-control',
         'onchange': "preview()",
         'name': 'filename'})

    class Meta:
        model = UserInfo
        fields = ('nickname', 'pfp')

class PostForSaleForm(forms.ModelForm):
    name = forms.CharField(max_length=100)    
    price = forms.IntegerField()
    createdAt = forms.DateTimeField()
    tags = forms.CharField()
    description = forms.CharField()
    upload = forms.ImageField();

    class Meta:
        model = Picture
        fields = ('name','price','createdAt','tags','description')

class PostCommentForm(forms.ModelForm):
    text = forms.CharField(max_length = 200,
                           widget=forms.widgets.TextInput(
                               attrs={
                                   'placeholder': 'Make a comment',
                                   'class': 'input-comment',
                               }),
                           label=''
                           )

    class Meta:
        model = Comment
        fields = ('text',)


