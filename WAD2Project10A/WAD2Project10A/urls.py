"""WAD2Project10A URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from OnlyPics import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sites.models import Site

hosted_site = Site.objects.all()[0]

urlpatterns = [
    path('', views.redirect_to_index, name="index"),
    path('onlypics/', include("OnlyPics.urls")),
    path('microsoft/', include('microsoft_auth.urls', namespace='microsoft')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "pythonanywhere" in hosted_site.domain:
    from WAD2Project10A import github
    urlpatterns.append(path('github_web_hook', github.update))
