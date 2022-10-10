from dataclasses import field, fields
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ('username', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        # veya '__all__' ve user i hariç tutmalıyız k aynısı olmasın exclude=('user')
        fields = ("portfolio", "profile_pic")


