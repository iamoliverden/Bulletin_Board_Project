from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Country, GameGenre, GamingPlatform, UserProfile, AdType, UserAds, AdReactions
from .serializers import CountrySerializer, GameGenreSerializer, GamingPlatformSerializer, UserProfileSerializer, AdTypeSerializer, UserAdsSerializer, AdReactionsSerializer

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class GameGenreViewSet(viewsets.ModelViewSet):
    queryset = GameGenre.objects.all()
    serializer_class = GameGenreSerializer

class GamingPlatformViewSet(viewsets.ModelViewSet):
    queryset = GamingPlatform.objects.all()
    serializer_class = GamingPlatformSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class AdTypeViewSet(viewsets.ModelViewSet):
    queryset = AdType.objects.all()
    serializer_class = AdTypeSerializer

class UserAdsViewSet(viewsets.ModelViewSet):
    queryset = UserAds.objects.all()
    serializer_class = UserAdsSerializer

class AdReactionsViewSet(viewsets.ModelViewSet):
    queryset = AdReactions.objects.all()
    serializer_class = AdReactionsSerializer

