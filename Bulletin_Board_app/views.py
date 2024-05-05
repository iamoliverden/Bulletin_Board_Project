from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework import viewsets
from .models import Country, GameGenre, GamingPlatform, UserProfile, AdType, UserAds, AdReactions
from .serializers import CountrySerializer, GameGenreSerializer, GamingPlatformSerializer, UserProfileSerializer, AdTypeSerializer, UserAdsSerializer, AdReactionsSerializer
from django.shortcuts import render
from .forms import UserForm, UserProfileForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy



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

# My Account Page
def my_account(request):
    my_ads = UserAds.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_account.html', {'my_ads': my_ads})

# Reactions Page
def reactions(request, ad_id):
    reactions = AdReactions.objects.filter(user_ad__id=ad_id)
    return render(request, 'reactions.html', {'reactions': reactions})

# Login Page
def login_view(request):
    # your login logic goes here
    return render(request, 'login.html')

def contact(request):
    return render(request, 'contact_us.html')

class UserProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'create_profile.html'
    second_form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        form2 = self.second_form_class(self.request.POST)
        if form2.is_valid():
            user = form2.save()
            self.object.user = user
            self.object.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.object.pk})