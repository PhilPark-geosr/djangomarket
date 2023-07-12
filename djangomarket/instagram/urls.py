from django.urls import path, include
from . import views

#URL Reverse에서 namespace역할
app_name = 'instagram' 


urlpatterns = [
    # URL reverse : name인자에 url리버스를 수행할 이름을 넘겨주면된다!

    # create view
    # path('ai/inference/new/', views.ai_new, name = "ai_new"),
    path('new/', views.post_new, name = "post_new"),
    
    # list view
    # path('ai/inference/', views.ai_list, name = "ai_list"),
    path('', views.post_list, name = "post_list"),

    # detail view
    path('<int:pk>/', views.post_detail, name = "post_detail"),
    
    # edit view
    path('<int:pk>/edit/', views.post_edit, name = "post_edit"),

]
