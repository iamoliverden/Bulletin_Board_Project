# view.py
import datetime
import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import CreateView
from django.forms import modelformset_factory
from functools import wraps
from rest_framework import viewsets

from .forms import *
from .serializers import *


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
    category = request.GET.get('category', '')
    date = request.GET.get('date', '')
    ads = UserAds.objects.exclude(user=request.user)
    if category:
        ads = ads.filter(ad_type__type_name=category)
    if date:
        ads = ads.filter(created_at__date=date)
    ads = ads.order_by('-created_at')
    categories = AdCategory.objects.all()

    # Add reaction statuses to each ad
    for ad in ads:
        ad.user_reaction_status = 'No Reaction'
        try:
            reaction = AdReactions.objects.filter(user_ad=ad, reacted_user=request.user).latest('reaction_time')
            if reaction.accepted_status == 1:
                ad.user_reaction_status = 'Reaction Sent'
            elif reaction.rejected_status == 1:
                ad.user_reaction_status = 'Reaction Withdrawn'
        except AdReactions.DoesNotExist:
            pass

    return render(request, 'landing.html', {'ads': ads, 'categories': categories})


# Landing Page for Non-Registered Users
def landing_page_non_registered(request):
    ads = UserAds.objects.all().order_by('-created_at')
    return render(request, 'landing_page_non_registered.html', {'ads': ads})


# Login Page
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Generate one-time code and send it to user's email
            code = str(random.randint(100000, 999999))
            send_mail(
                'Your one-time code',
                f'Your one-time code is {code}',
                settings.EMAIL_HOST_USER,  # sender email
                [user.email],
                fail_silently=False,
            )
            request.session['one_time_code'] = code
            request.session['code_generation_time'] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            request.session['user_id'] = user.id
            return redirect('enter_one_time_code')
    return render(request, 'login.html')


def enter_one_time_code(request):
    if request.method == 'POST':
        code = request.POST['code']
        if code == request.session.get('one_time_code'):
            code_generation_time = datetime.datetime.strptime(request.session.get('code_generation_time'),
                                                              "%m/%d/%Y, %H:%M:%S")
            if datetime.datetime.now() - code_generation_time < datetime.timedelta(minutes=2):
                user = User.objects.get(id=request.session.get('user_id'))
                # Specify the backend directly
                backend = 'django.contrib.auth.backends.ModelBackend'
                user.backend = backend
                login(request, user)
                try:
                    UserProfile.objects.get(user=user)
                    return redirect('my_account')  # if profile exists, redirect to 'my_account'
                except UserProfile.DoesNotExist:
                    return redirect('create_profile')  # if profile does not exist, redirect to 'create_profile'
            else:
                messages.error(request, 'The one-time code has expired. Please try again.')
        else:
            messages.error(request, 'The one-time code is incorrect. Please try again.')
    return render(request, 'enter_one_time_code.html')


def contact(request):
    return render(request, 'contact_us.html')


@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
class UserProfileCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'create_profile.html'

    def get_context_data(self, **kwargs):
        data = super(UserProfileCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['social_media_forms'] = UserProfileForm.social_media_forms(self.request.POST, instance=self.object)
        else:
            data['social_media_forms'] = UserProfileForm.social_media_forms(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        social_media_forms = context['social_media_forms']
        if social_media_forms.is_valid():
            form.instance.user = self.request.user  # set user to the currently logged in user
            self.object = form.save()
            social_media_forms.instance = self.object
            social_media_forms.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('my_account')


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
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
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        social_media_forms = UserProfileForm.social_media_forms(request.POST, instance=request.user.userprofile)
        if form.is_valid() and social_media_forms.is_valid():
            form.save()
            social_media_forms.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('my_account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
        social_media_forms = UserProfileForm.social_media_forms(instance=request.user.userprofile)
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


@login_required
@profile_required
def ads_view(request):
    category = request.GET.get('category', '')
    date = request.GET.get('date', '')
    user_ads = UserAds.objects.filter(user=request.user)
    if category:
        user_ads = user_ads.filter(ad_type__type_name=category)
    if date:
        user_ads = user_ads.filter(created_at__date=date)
    user_ads = user_ads.order_by('-created_at')
    categories = AdCategory.objects.all()
    return render(request, 'ads.html', {'user_ads': user_ads, 'categories': categories})


@login_required
@profile_required
def create_ad_view(request):
    MediaFileFormSet = modelformset_factory(MediaFile, form=MediaFileForm, extra=3)
    if request.method == 'POST':
        form = UserAdsForm(request.POST, request.FILES)
        formset = MediaFileFormSet(request.POST, request.FILES, queryset=MediaFile.objects.none())
        if form.is_valid() and formset.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            for media_form in formset:
                media_file = media_form.save(commit=False)
                media_file.user_ad = ad
                media_file.save()
            return redirect('ads')
    else:
        form = UserAdsForm()
        formset = MediaFileFormSet(queryset=MediaFile.objects.none())
    return render(request, 'create_ad.html', {'form': form, 'formset': formset})


@login_required
@profile_required
def edit_ad_view(request, ad_id):
    ad = UserAds.objects.get(id=ad_id, user=request.user)
    MediaFileFormSet = modelformset_factory(MediaFile, form=MediaFileForm, extra=3, max_num=3)
    if request.method == 'POST':
        form = UserAdsForm(request.POST, request.FILES, instance=ad)  # include request.FILES
        formset = MediaFileFormSet(request.POST, request.FILES, queryset=MediaFile.objects.filter(user_ad=ad))
        if form.is_valid() and formset.is_valid():
            form.save()
            for media_form in formset:
                media_file = media_form.save(commit=False)
                media_file.user_ad = ad
                media_file.save()
            return redirect('ads')
    else:
        form = UserAdsForm(instance=ad)
        formset = MediaFileFormSet(queryset=MediaFile.objects.filter(user_ad=ad))
    return render(request, 'edit_ad.html', {'form': form, 'formset': formset})


@login_required
@profile_required
def delete_ad_view(request, ad_id):
    ad = UserAds.objects.get(id=ad_id, user=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('ads')
    return render(request, 'delete_ad.html', {'ad': ad})


@login_required
@profile_required
def received_reactions(request):
    user_ads = UserAds.objects.filter(user=request.user)
    reactions = AdReactions.objects.filter(user_ad__in=user_ads)
    return render(request, 'received_reactions.html', {'reactions': reactions})


@login_required
@profile_required
def sent_reactions(request):
    reactions = AdReactions.objects.filter(reacted_user=request.user)
    return render(request, 'sent_reactions.html', {'reactions': reactions})


@login_required
@profile_required
def update_reaction(request, reaction_id):
    reaction = AdReactions.objects.get(id=reaction_id)
    if 'accept' in request.POST:
        reaction.accepted_status = True
        reaction.rejected_status = False
    elif 'reject' in request.POST:
        reaction.accepted_status = False
        reaction.rejected_status = True
    reaction.save()
    return redirect('received_reactions')


def logout_view(request):
    logout(request)
    return redirect('landing_page_non_registered')  # or your desired redirect page


@login_required
@profile_required
def accept_ad(request, ad_id):
    if request.method == 'POST':
        form = AdReactionForm(request.POST)
        if form.is_valid():
            reaction = form.save(commit=False)
            reaction.user_ad = UserAds.objects.get(id=ad_id)
            reaction.reacted_user = request.user
            reaction.accepted_status = True
            reaction.rejected_status = False
            reaction.save()
            return redirect('landing_page_registered')
    else:
        form = AdReactionForm()
    return render(request, 'create_reaction.html', {'form': form, 'ad_id': ad_id})


@login_required
@profile_required
def reject_ad(request, ad_id):
    AdReactions.objects.create(user_ad=UserAds.objects.get(id=ad_id), reacted_user=request.user, accepted_status=False,
                               rejected_status=True)
    return redirect('landing_page_registered')


@login_required
@profile_required
def delete_reaction(request, reaction_id):
    reaction = AdReactions.objects.get(id=reaction_id, reacted_user=request.user)
    reaction.delete()
    return redirect('sent_reactions')


@login_required
@profile_required
def accept_reaction(request, reaction_id):
    reaction = AdReactions.objects.get(id=reaction_id, user_ad__user=request.user)
    reaction.reaction_received_status = 1
    reaction.save()
    return redirect('received_reactions')


@login_required
@profile_required
def ignore_reaction(request, reaction_id):
    reaction = AdReactions.objects.get(id=reaction_id, user_ad__user=request.user)
    reaction.reaction_received_status = 2
    reaction.save()
    return redirect('received_reactions')


def handle_reaction_received(reaction):
    # Send email to ad author
    ad_author_email = reaction.user_ad.user.email
    subject = 'You received a new reaction'
    body = f'You received a new reaction to your ad "{reaction.user_ad.title}". The message is: "{reaction.reaction_text}".'
    send_mail(subject, body, settings.EMAIL_HOST_USER, [ad_author_email])


def handle_reaction_accepted(reaction):
    # Send email to reaction author
    reaction_author_email = reaction.reacted_user.email
    subject = 'Your reaction was accepted'
    body = f'Your reaction to the ad "{reaction.user_ad.title}" was accepted. Please contact the ad author using their preferred method of contact: {reaction.user_ad.user.userprofile.communication_preference.preference}.'
    send_mail(subject, body, settings.EMAIL_HOST_USER, [reaction_author_email])


def ad_detail_view(request, ad_id):
    ad = UserAds.objects.get(id=ad_id)
    return render(request, 'ad_detail.html', {'ad': ad})
