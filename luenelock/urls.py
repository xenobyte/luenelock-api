"""luenelock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.authtoken import views as auth_views

from api import views

urlpatterns = [
    path('', views.readme, name='readme'),
    path('admin/', admin.site.urls),
    path('api/locks', views.LockList.as_view(), name='lock-list'),
    path('api/locks/<uuid:uuid>', views.LockDetail.as_view(), name='lock-detail'),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('accounts/profile/', RedirectView.as_view(url='/api/locks')),
]
