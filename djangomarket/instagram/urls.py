from django.urls import path, include
from . import views
urlpatterns = [
    path('ai/', views.ai_new, name = "ai_new"),
    path('new/', views.post_new, name = "post_new"),
    path('', views.post_list),
]
