from django import forms
from blog import models


class UserModelForm(forms.ModelForm):
    class Meta():
        model = models.User
        fields = ('username', 'email', 'password')


class UserProfileModelForm(forms.ModelForm):
    class Meta():
        model = models.UserProfile
        fields = ('prof_url', 'prof_pic')


class CommentModelForm(forms.ModelForm):
    class Meta():
        model = models.Comment
        fields = ('author', 'text')
