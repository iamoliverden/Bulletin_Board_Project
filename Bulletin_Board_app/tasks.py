from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import UserAds
from datetime import datetime, timedelta

def generate_digest_for_user(user):
    # Get the date one week ago
    one_week_ago = datetime.now() - timedelta(weeks=1)

    # Get the latest ads posted in the past week
    latest_ads = UserAds.objects.filter(created_at__gte=one_week_ago)

    # Generate the digest
    digest = 'Hello, ' + user.username + '\n\n'
    digest += 'Here is your weekly digest of the latest ads:\n\n'
    for ad in latest_ads:
        digest += ad.title + '\n'
    digest += '\nThank you for using our service!'

    return digest


def send_weekly_digest():
    users = User.objects.filter(userprofile__news_digest=True)
    for user in users:
        digest = generate_digest_for_user(user)  # You'll need to implement this function
        send_mail(
            'Your weekly digest',
            digest,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_weekly_digest, 'cron', day_of_week='tue', hour=10)
    scheduler.start()
