"""config URL Configuration

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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = [
    path('', include("accounts.urls")),
    path('', include("items.urls")),
    path('information/', TemplateView.as_view(template_name='information/information.html'), name='information'),
    path('admin/', admin.site.urls),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.IMAGE_URL, document_root=settings.IMAGE_ROOT)
if not settings.DEBUG:
    urlpatterns += static(settings.CERT_URL, document_root=settings.CERT_ROOT)