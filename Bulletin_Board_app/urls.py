# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *

router = DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'gamegenres', views.GameGenreViewSet)
router.register(r'gamingplatforms', views.GamingPlatformViewSet)
router.register(r'adtypes', views.AdTypeViewSet)
router.register(r'userads', views.UserAdsViewSet)
router.register(r'adreactions', views.AdReactionsViewSet)
router.register(r'userprofiles', views.UserProfileViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('landing/', views.landing_page_registered, name='landing_page_registered'),
    path('non_registered/', views.landing_page_non_registered, name='landing_page_non_registered'),
    path('my_account/', views.my_account, name='my_account'),
    path('reactions/<int:ad_id>/', views.reactions, name='reactions'),
    path('login/', views.login_view, name='login'),  # login view
    path('contact_us/', views.contact, name='contact_us'),
    path('create_profile/', UserProfileCreateView.as_view(), name='create_profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
