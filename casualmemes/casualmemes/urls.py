"""casualmemes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from meme_page import views as ex_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("memes/<genre>", ex_views.MenuView.as_view(), name="menu"),
    path("", ex_views.RedirectView.as_view(), name="index"),
    path("meme/create/", ex_views.MemeCreateView.as_view(), name="create-meme"),
    path("avatar/change/", ex_views.AvatarChangeView.as_view(), name="change-avatar"),
    path("user/create/", ex_views.AddUserView.as_view(), name="create-user"),
    path(
        "meme/report/<int:report_id>",
        ex_views.CreateReportView.as_view(),
        name="create-report",
    ),
    path(
        "accounts/password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change.html"
        ),
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
