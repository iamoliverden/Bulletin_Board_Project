# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from ckeditor.widgets import CKEditorWidget
from .models import *


class UserSocialMediaForm(forms.ModelForm):
    class Meta:
        model = UserSocialMedia
        fields = ('social_media_key', 'handle')


class UserProfileForm(forms.ModelForm):
    social_media_forms = forms.inlineformset_factory(UserProfile, UserSocialMedia, form=UserSocialMediaForm, extra=3)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'placeholder': 'YYYY-MM-DD'}),
        input_formats=('%Y-%m-%d',),
        error_messages={
            'invalid': 'Enter a valid date in YYYY-MM-DD format.',
        }
    )
    country = forms.ModelChoiceField(queryset=Country.objects.all())
    favorite_game_genre = forms.ModelChoiceField(queryset=GameGenre.objects.all())
    gaming_platform = forms.ModelChoiceField(queryset=GamingPlatform.objects.all())
    communication_preference = forms.ModelChoiceField(queryset=CommunicationPreference.objects.all())

    class Meta:
        model = UserProfile
        fields = (
            'date_of_birth', 'mobile_number', 'country', 'favorite_game_genre', 'gaming_platform', 'privacy_consent',
            'news_digest', 'biography', 'communication_preference', 'profile_picture')


class UserAdsForm(forms.ModelForm):
    rich_text = forms.CharField(widget=CKEditorWidget())  # new field for the rich text content

    class Meta:
        model = UserAds
        fields = ['title', 'ad_text', 'rich_text', 'ad_type', 'picture', 'video_link']

    def __init__(self, *args, **kwargs):
        super(UserAdsForm, self).__init__(*args, **kwargs)
        self.fields['ad_type'].queryset = AdCategory.objects.all()


class AdReactionForm(forms.ModelForm):
    class Meta:
        model = AdReactions
        fields = ['reaction_text']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
