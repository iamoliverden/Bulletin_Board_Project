# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('date_of_birth', 'mobile_number', 'country', 'fav_game_genre', 'gaming_platform', 'privacy_consent', 'news_digest', 'social_media', 'biography', 'communication_preference', 'profile_picture')
