from django.urls import path, include
from . import views
urlpatterns = [
    path('ai/inference/new/', views.ai_new, name = "ai_new"),
    path('ai/inference/', views.ai_list, name = "ai_list"),
    path('new/', views.post_new, name = "post_new"),
    path('', views.post_list),
]
