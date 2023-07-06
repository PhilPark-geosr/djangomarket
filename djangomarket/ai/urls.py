from django.urls import path, include
from . import views

app_name = 'ai'

urlpatterns = [
    path('inference/new/', views.ai_new, name = "ai_new"),
    path('inference/', views.ai_list, name = "ai_list"),

    path('inference/detail/new/', views.aidetail_new, name = "aidetail_new"),
    # path('inference/detail/', views.aidetail_list, name = "aidetail_list"),
    
]
