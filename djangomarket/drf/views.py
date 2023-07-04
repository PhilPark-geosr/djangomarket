from django.shortcuts import render

# DRF 
from rest_framework import generics
# DRF -view
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
# DRF - Response
from rest_framework.response import Response
# DRF - Decorator
from rest_framework.decorators import api_view

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



# V1 generics의 List APIView 사용한 버전
# class PublicPostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.filter(is_public = True)
#     serializer_class = PostSerializer

# V2 APIView로 멤버함수 구현한 버전
# class PublicPostListAPIView(APIView):
#     def get(self, request, format=None):
#         qs = Post.objects.filter(is_public = True)
#         serializer = PostSerializer(qs, many =True)
#         return Response(serializer.data) #이렇게 해야 HTTPresponse로 감싸져서 나온다
# # 함수로 따로 정의
# public_post_list = PublicPostListAPIView.as_view()

# V3 함수기반뷰 
'''
1) api_view로 장식자 붙임
2) 나머지는 APIView위 멤버함수인 get함수와 동일하게 구성
'''
@api_view(['GET'])
def public_post_list(request):
    qs = Post.objects.filter(is_public = True)
    serializer = PostSerializer(qs, many =True)
    return Response(serializer.data) #이렇게 해야 HTTPresponse로 감싸져서 나온다