from django.urls import path, include
from . import views

# DRF 
from rest_framework.routers import DefaultRouter

# viewset 추가할 ㅣ경우 
router = DefaultRouter()
router.register('post', views.PostViewSet) # 2개 URL패턴 만들어줌

print("router.urls", router.urls) ## URL pattern list
#URL Reverse에서 namespace역할
app_name = 'drf' 

urlpatterns = [
    # path('public/', views.PublicPostListAPIView.as_view()),
    path('public/', views.public_post_list),
    path('', include(router.urls)),
    
]
