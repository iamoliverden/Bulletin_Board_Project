# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5)

    def __str__(self):
        return self.country_name

class GameGenre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name

class GamingPlatform(models.Model):
    platform_name = models.CharField(max_length=100)

    def __str__(self):
        return self.platform_name


class CommunicationPreference(models.Model):
    preference = models.CharField(max_length=20)

    def __str__(self):
        return self.preference

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    favorite_game_genre = models.ForeignKey(GameGenre, on_delete=models.CASCADE, null=True, blank=True)
    gaming_platform = models.ForeignKey(GamingPlatform, on_delete=models.CASCADE, null=True, blank=True)
    privacy_consent = models.BooleanField(default=False)
    news_digest = models.BooleanField(default=False)
    biography = models.TextField(max_length=500, blank=True, null=True)
    communication_preference = models.ForeignKey(CommunicationPreference, on_delete=models.CASCADE, default=1)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


class AdCategory(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name

class UserAds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad_type = models.ForeignKey(AdCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to='ad_pictures/', blank=True, null=True)  # new field for the picture
    video_link = models.URLField(max_length=200, blank=True, null=True)  # new field for the video link
    ad_text = models.TextField(max_length=500, default='')
    title = models.CharField(max_length=200, default='')

class AdReactions(models.Model):
    user_ad = models.ForeignKey(UserAds, on_delete=models.CASCADE)
    reacted_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_time = models.DateTimeField(default=timezone.now)
    accepted_status = models.BooleanField(default=False)
    rejected_status = models.BooleanField(default=False)
    reaction_text = models.TextField(blank=True, null=True, max_length=500)


class SocialMedia(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserSocialMedia(models.Model):
    profile_key = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    social_media_key = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    handle = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user_profile.user.username} - {self.social_media.name}'
