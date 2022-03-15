from django import forms
from OnlyPics.models import UserInfo

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