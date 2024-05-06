# forms.py
from django import forms
from .models import *

class UserSocialMediaForm(forms.ModelForm):
    class Meta:
        model = UserSocialMedia
        fields = ('social_media', 'handle')
class UserProfileForm(forms.ModelForm):
    social_media_forms = forms.inlineformset_factory(UserProfile, UserSocialMedia, form=UserSocialMediaForm, extra=1)
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
        fields = ('date_of_birth', 'mobile_number', 'country', 'favorite_game_genre', 'gaming_platform', 'privacy_consent', 'news_digest', 'biography', 'communication_preference', 'profile_picture')