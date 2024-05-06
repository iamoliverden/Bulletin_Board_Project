# view.py
from rest_framework import viewsets
from rest_framework import generics
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

class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

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

# Landing Page for Registered Users
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
                return redirect('my_account')  # assuming 'my_account' is the name of your my account view
            except UserProfile.DoesNotExist:
                return redirect('create_profile')  # assuming 'complete_profile' is the name of your profile completion view
    return render(request, 'login.html')

def contact(request):
    return render(request, 'contact_us.html')



@method_decorator(login_required, name='dispatch')
class UserProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'complete_profile.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['social_media_forms'] = self.form_class.social_media_forms(self.request.POST, instance=self.object)
        else:
            data['social_media_forms'] = self.form_class.social_media_forms(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        social_media_forms = context['social_media_forms']
        if form.is_valid() and social_media_forms.is_valid():
            self.object = form.save()
            social_media_forms.instance = self.object
            social_media_forms.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my_account')  # assuming 'my_account' is the name of your my account view
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # assuming 'login' is the name of your login view
    template_name = 'signup.html'


# My Account Page
@login_required
def my_account(request):
    user_profile = UserProfile.objects.get(user=request.user)
    my_ads = UserAds.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_account.html', {'user_profile': user_profile, 'my_ads': my_ads})

# Reactions Page
def reactions(request, ad_id):
    reactions = AdReactions.objects.filter(user_ad__id=ad_id)
    return render(request, 'reactions.html', {'reactions': reactions})