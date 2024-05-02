# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5)

class GameGenre(models.Model):
    genre_name = models.CharField(max_length=100)

class GamingPlatform(models.Model):
    platform_name = models.CharField(max_length=100)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=15)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    fav_game_genre = models.ForeignKey(GameGenre, on_delete=models.CASCADE)
    gaming_platform = models.ForeignKey(GamingPlatform, on_delete=models.CASCADE)
    privacy_consent = models.BooleanField(default=False)
    news_digest = models.BooleanField(default=False)
    social_media = models.JSONField()
    biography = models.TextField(max_length=500, blank=True, null=True)
    communication_preference = models.CharField(choices=[('EMAIL', 'Email'), ('PHONE', 'Phone'), ('TELEKINESIS', 'telekinesis')], default='EMAIL', max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

class AdType(models.Model):
    type_name = models.CharField(max_length=100)

class UserAds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad_type = models.ForeignKey(AdType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class AdReactions(models.Model):
    user_ad = models.ForeignKey(UserAds, on_delete=models.CASCADE)
    reacted_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_time = models.DateTimeField(default=timezone.now)
    accepted_status = models.BooleanField(default=False)
