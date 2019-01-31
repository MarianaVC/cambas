"""cambas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from ajax_select import urls as ajax_select_urls
from . import views
admin.site.site_header = "Cambas Admin"
admin.site.site_title = "Cambas Admin Portal"
admin.site.index_title = "Welcome to Cambas Admin Portal :) "
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^sing-up/$',views.sing_up,name='sing_up'),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS    
    url(r'^admin/', admin.site.urls),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^users/', include('users.urls')),
    url(r'^api/v0/', include('users.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
