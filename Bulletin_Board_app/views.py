# view.py
from rest_framework import viewsets
from .serializers import *
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserSocialMediaForm
from functools import wraps

def profile_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return redirect('create_profile')  # or your profile creation view
        return view_func(request, *args, **kwargs)
    return wrapper

# REST API Views
@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
@method_decorator(profile_required, name='dispatch')
class UserAdsViewSet(viewsets.ModelViewSet):
    queryset = UserAds.objects.all()
    serializer_class = UserAdsSerializer

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
@method_decorator(profile_required, name='dispatch')
class AdReactionsViewSet(viewsets.ModelViewSet):
    queryset = AdReactions.objects.all()
    serializer_class = AdReactionsSerializer

# Django Templates
@login_required
@profile_required
def landing_page_registered(request):
    ads = UserAds.objects.all().order_by('-created_at')
    return render(request, 'landing.html', {'ads': ads})


# Landing Page for Non-Registered Users
def landing_page_non_registered(request):
    ads = UserAds.objects.all().order_by('-created_at')
    return render(request, '403.html', {'ads': ads})

# Login Page
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                UserProfile.objects.get(user=user)
                return redirect('my_account')  # if profile exists, redirect to 'my_account'
            except UserProfile.DoesNotExist:
                return redirect('create_profile')  # if profile does not exist, redirect to 'create_profile'
    return render(request, 'login.html')

def contact(request):
    return render(request, 'contact_us.html')

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class UserProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'complete_profile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # set user to the currently logged in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_account')  # assuming 'my_account' is the name of your my account view

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # assuming 'login' is the name of your login view
    template_name = 'signup.html'

# My Account Page
@login_required
@profile_required
def my_account(request):
    user_profile = UserProfile.objects.get(user=request.user)
    my_ads = UserAds.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_account.html', {'user_profile': user_profile, 'my_ads': my_ads})

# Reactions Page
@login_required
@profile_required
def reactions(request, ad_id):
    reactions = AdReactions.objects.filter(user_ad__id=ad_id)
    return render(request, 'reactions.html', {'reactions': reactions})

# Edit Profile Page
@login_required
@profile_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.userprofile)
        social_media_forms = UserSocialMediaForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and social_media_forms.is_valid():
            form.save()
            social_media_forms.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('my_account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
        social_media_forms = UserSocialMediaForm(instance=request.user.userprofile)
    return render(request, 'edit_profile.html', {'form': form, 'social_media_forms': social_media_forms})

# Delete Profile Page
@login_required
@profile_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account was successfully deleted!')
        return redirect('landing_page_non_registered')
    return render(request, 'delete_profile.html')

# Ads Page
@login_required
@profile_required
def ads(request):
    user_ads = UserAds.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ads.html', {'user_ads': user_ads})

# Reactions Page
@login_required
@profile_required
def reactions(request):
    user_reactions = AdReactions.objects.filter(reacted_user=request.user)
    return render(request, 'reactions.html', {'user_reactions': user_reactions})

