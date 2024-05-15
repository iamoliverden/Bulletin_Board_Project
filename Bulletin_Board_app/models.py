# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_email_notification
from ckeditor.fields import RichTextField


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
    biography = RichTextField(blank=True, null=True, max_length=500)
    communication_preference = models.ForeignKey(CommunicationPreference, on_delete=models.CASCADE, default=1)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def delete(self, *args, **kwargs):
        self.profile_picture.delete(save=False)  # delete profile_picture file
        super().delete(*args, **kwargs)  # call the original delete method


class AdCategory(models.Model):
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name


class UserAds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad_type = models.ForeignKey(AdCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    ad_text = RichTextField(blank=True, null=True, max_length=500)
    title = models.CharField(max_length=200, blank=False, null=False)

    def delete(self, *args, **kwargs):
        for media_file in self.media_files.all():
            # delete the file associated with the MediaFile instance
            if media_file.media_file:
                media_file.media_file.delete()
            # delete the MediaFile instance
            media_file.delete()
        super().delete(*args, **kwargs)  # call the original delete method


class MediaFile(models.Model):
    user_ad = models.ForeignKey(UserAds, related_name='media_files', on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='media_files/', blank=True, null=True)

    def __str__(self):
        return f'Media file for ad {self.user_ad.title}'


class AdReactions(models.Model):
    user_ad = models.ForeignKey(UserAds, on_delete=models.CASCADE)
    reacted_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_time = models.DateTimeField(default=timezone.now)
    accepted_status = models.BooleanField(default=False)
    rejected_status = models.BooleanField(default=False)
    reaction_text = models.TextField(blank=True, null=True, max_length=500)
    reaction_received_status = models.IntegerField(default=0)


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


@receiver(post_save, sender=AdReactions)
def post_save_adreaction(sender, instance, created, **kwargs):
    if created:
        # Send email to ad author
        ad_author_email = instance.user_ad.user.email
        subject = 'You received a new reaction'
        body = f'You received a new reaction to your ad "{instance.user_ad.title}".\n\n' \
               f'The message is: "{instance.reaction_text}".\n\n' \
               f'The reaction was from {instance.reacted_user.username} in {instance.reacted_user.userprofile.country}.\n\n' \
               f'Their preferred method of contact is: {instance.reacted_user.userprofile.communication_preference.preference}.\n\n' \
               f'You can wait for them to contact you, or you can contact them directly.'
        send_email_notification(subject, body, ad_author_email)
    elif instance.accepted_status:
        # Send email to reaction author
        reaction_author_email = instance.reacted_user.email
        subject = 'Your reaction was accepted'
        body = f'Your reaction to the ad "{instance.user_ad.title}" was accepted. Please contact the ad author using their preferred method of contact: {instance.user_ad.user.userprofile.communication_preference.preference}.'
        send_email_notification(subject, body, reaction_author_email)
