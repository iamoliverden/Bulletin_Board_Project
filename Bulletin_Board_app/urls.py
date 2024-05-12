# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *


router = DefaultRouter()
router.register(r'userads', views.UserAdsViewSet, basename='userads_rest')
router.register(r'adreactions', views.AdReactionsViewSet, basename='adreactions_rest')

urlpatterns = [
    path('my_api', include(router.urls)),
    path('landing/', views.landing_page_registered, name='landing_page_registered'),
    path('non_registered/', views.landing_page_non_registered, name='landing_page_non_registered'),
    path('my_account/', views.my_account, name='my_account'),
    path('reactions/<int:ad_id>/', views.reactions, name='reactions'),
    path('contact_us/', views.contact, name='contact_us'),
    path('create_profile/', UserProfileCreateView.as_view(), name='create_profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('ads/', ads_view, name='ads'),
    path('ads/create/', create_ad_view, name='create_ad'),
    path('ads/edit/<int:ad_id>/', edit_ad_view, name='edit_ad'),
    path('ads/delete/<int:ad_id>/', delete_ad_view, name='delete_ad'),
    path('logout/', views.logout_view, name='logout'),
    path('received_reactions/', views.received_reactions, name='received_reactions'),
    path('sent_reactions/', views.sent_reactions, name='sent_reactions'),
    path('update_reaction/<int:reaction_id>/', views.update_reaction, name='update_reaction'),
    path('accept_ad/<int:ad_id>/', views.accept_ad, name='accept_ad'),
    path('reject_ad/<int:ad_id>/', views.reject_ad, name='reject_ad'),
    path('delete_reaction/<int:reaction_id>/', views.delete_reaction, name='delete_reaction'),
    path('accept_reaction/<int:reaction_id>/', views.accept_reaction, name='accept_reaction'),
    path('ignore_reaction/<int:reaction_id>/', views.ignore_reaction, name='ignore_reaction'),
    path('ads/<int:ad_id>/', views.ad_detail_view, name='ad_detail'),

]
