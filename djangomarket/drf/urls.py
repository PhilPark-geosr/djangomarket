from django.urls import path, include
from . import views

# DRF viewset을 등록할 경우...!
from rest_framework.routers import DefaultRouter

# viewset 추가할 ㅣ경우 
router = DefaultRouter()
router.register('post', views.PostViewSet) # 2개 URL패턴 만들어줌
# router.register('ai', views.AIDetailViewSet)

# ModelViewset 적용
memo_list = views.AIDetailViewSet.as_view(
    {"get": "list", "post": "set_content"})
memo_detail = views.AIDetailViewSet.as_view(
    {"get": "retrieve", "patch": "partial_update", "delete": "destroy"})

# print("router.urls", router.urls) ## URL pattern list
'''
[<URLPattern '^post/$' [name='post-list']>, <URLPattern '^post\.(?P<format>[a-z0-9]+)/?$' [name='post-list']>, <URLPattern '^post/(?P<pk>[^/.]+)/$' [name='post-detail']>, <URLPattern '^post/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='post-detail']>, <URLPattern '^$' [name='api-root']>, <URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>]
'''

#URL Reverse에서 namespace역할
app_name = 'drf' 

urlpatterns = [
    # path('public/', views.PublicPostListAPIView.as_view()),
    path('public/', views.public_post_list),
    path('', include(router.urls)),
    # path('ai/', views.aidetail_list)
    path('ai/', memo_list),
    path('ai/<int:pk>', memo_detail)
    
]
