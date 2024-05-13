"""
URL configuration for Bulletin_Board_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py project
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import Bulletin_Board_app.views as views

urlpatterns = [
    path('admin/', admin.site.urls),  # replace 'your_app_name' with the name of your Django app
    path('app/', include('Bulletin_Board_app.urls')),
    path('login/', views.login_view, name='login'),  # login view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)