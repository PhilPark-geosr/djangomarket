from django.urls import path, include
from . import views

#URL Reverse에서 namespace역할
app_name = 'instagram' 

urlpatterns = [
    path('ai/inference/new/', views.ai_new, name = "ai_new"),
    path('ai/inference/', views.ai_list, name = "ai_list"),
    path('new/', views.post_new, name = "post_new"),
    path('', views.post_list),

    # name인자에 url리버스를 수행할 이름을 넘겨주면된다!
    path('<int:pk>/', views.post_detail, name = "post_detail"),
]
