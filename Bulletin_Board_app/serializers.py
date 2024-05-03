# serializers.py
from rest_framework import serializers
from .models import Country, GameGenre, GamingPlatform, UserProfile, AdType, UserAds, AdReactions

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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

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
