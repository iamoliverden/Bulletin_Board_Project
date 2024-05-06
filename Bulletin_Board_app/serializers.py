# serializers.py
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class GameGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameGenre
        fields = '__all__'

class GamingPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamingPlatform
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        return user_profile

class AdTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdType
        fields = '__all__'

class UserAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAds
        fields = '__all__'

class AdReactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdReactions
        fields = '__all__'
