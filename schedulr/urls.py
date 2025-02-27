"""
URL configuration for schedulr project.

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

from django.contrib import admin
from django.urls import path

from schedulr.account.views import InitialSetupView, SessionSetupView
from schedulr.event.views import EventDetail, Homepage

urlpatterns = [
    path("", Homepage.as_view(), name="homepage"),
    path(
        "account/initial-setup",
        InitialSetupView.as_view(),
        name="initial-setup",
    ),
    path(
        "whoami",
        SessionSetupView.as_view(),
        name="whoami",
    ),
    path("admin/", admin.site.urls),
    path("event/<str:pk>", EventDetail.as_view(), name="event_detail"),
]
