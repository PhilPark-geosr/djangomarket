"""djangomarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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


"""
from django.conf import global_settings
from . import settings
"""
# 이렇게 해야 위 두개를 합쳐서 해준다
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog1/', include('blog1.urls')), 
    path('instagram/', include('instagram.urls')), 
    path('market/', include('market.urls')), 

]


if settings.DEBUG: #디버그 옵션 참일때만 수행, 즉 디버깅 모드에서만 접근 가능
    # MEDIA_URL로 이미지 접근 가능하게 함!
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

