# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'gamegenres', views.GameGenreViewSet)
router.register(r'gamingplatforms', views.GamingPlatformViewSet)
router.register(r'userprofiles', views.UserProfileViewSet)
router.register(r'adtypes', views.AdTypeViewSet)
router.register(r'userads', views.UserAdsViewSet)
router.register(r'adreactions', views.AdReactionsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
