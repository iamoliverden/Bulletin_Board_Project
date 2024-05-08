# serializers.py
from rest_framework import serializers
from .models import *


class UserAdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAds
        fields = '__all__'

class AdReactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdReactions
        fields = '__all__'
