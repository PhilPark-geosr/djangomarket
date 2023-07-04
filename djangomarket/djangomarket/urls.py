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
from django.conf.urls import url

# DRF and Swagger 관련
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi

"""
from django.conf import global_settings
from . import settings
"""
# 이렇게 해야 위 두개를 합쳐서 해준다
from django.conf import settings

from django.conf.urls.static import static
# View관련
# CBV
from django.views.generic import TemplateView, RedirectView

class RootView(TemplateView):
    template_name = 'root.html'


# Swagger로 보고 싶은 urls 추가
schema_url_patterns = [ 
    path('', include('drf.urls')),
    ]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Open API",
        default_version='v1',
        description="시스템 API",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)


# URL pattern 추가
urlpatterns = [
    # path('', RootView.as_view(template_name = "root.html"), name ='root'),
    # 리다이렉트 url = 원하는 이동경로
    path('', RedirectView.as_view(
        # url = '/instagram/'
        pattern_name = "instagram:post_list", #URL Reverse        
        ), name = 'root'), 
    path('admin/', admin.site.urls),

    # DRF
    path('api-auth/', include('rest_framework.urls')),

    # my app
    path('blog1/', include('blog1.urls')), 
    path('instagram/', include('instagram.urls')), 
    path('market/', include('market.urls')), 
    path('accounts/', include('accounts.urls')),
    path('ai/', include('ai.urls')), # for ai inference
    
    # DRF
    path('api/', include('drf.urls')), # drf
    
    # swagger
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG: #디버그 옵션 참일때만 수행, 즉 디버깅 모드에서만 접근 가능
    # MEDIA_URL로 이미지 접근 가능하게 함!
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

