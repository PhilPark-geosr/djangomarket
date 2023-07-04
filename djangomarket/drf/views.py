from django.shortcuts import render

# DRF view
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

# import Model
from .models import Post

# Serializer
from .serializers import PostSerializer

# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    # CBV에서 실제 요청이 올때마다 항상 소출되는 함수
    def dispatch(self, request, *args, **kwargs):
        print(f"request.body : {request.body}") #TODO: logger 사용
        print(f"request.POST : {request.POST}")
        return super().dispatch(request, *args, **kwargs)

class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer