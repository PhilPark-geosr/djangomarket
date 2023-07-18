from django.shortcuts import render, redirect

# DRF 
from rest_framework import generics, status
# DRF -view
from rest_framework.views import APIView
# post_list, post_detail 한꺼번에 지원해주는 viewset
from rest_framework.viewsets import ModelViewSet
# DRF - Response
from rest_framework.response import Response
# DRF - Decorator
from rest_framework.decorators import api_view, action

# import Model
from .models import Post, AIDetail

# Serializer
from .serializers import PostSerializer, AIDetailSerializer

from rest_framework.renderers import TemplateHTMLRenderer
# 다른 웹서버에 자료 요청용
import requests
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



# ---------------------------------- for AI --------------------------------- #
class AIDetailViewSet(ModelViewSet):
    queryset = AIDetail.objects.all()
    serializer_class = AIDetailSerializer

    # def list(self, request):
    #     pass
    # def create(self, request):
    #     pass
    #TODO: action 추가로직 구현
    @action(detail=False, methods=['post'])
    def set_content(self, request):
        serializer = AIDetailSerializer(data=request.data)
        # print("request.POST",request.POST)
        if serializer.is_valid():

            # 추론서버에 데이터 요청
            files = request.FILES['photo']
            upload = {'image': files}

            url = 'http://192.168.1.141:8000/inference/'
            res = requests.post(url, files = upload) # 요청한 결과 res에 받음

            # 데이터 추가 저장
            serializer.save(user=request.user, result=res.json()) #추가로 넣어주고 싶은 데이터를 키워드 인자로 넣어준다!
            # print('savecomplete')
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    # CBV에서 실제 요청이 올때마다 항상 소출되는 함수
    def dispatch(self, request, *args, **kwargs):
        print(f"request.body : {request.body}") #TODO: logger 사용
        print(f"request.POST : {request.POST}")
        return super().dispatch(request, *args, **kwargs)

# class AIDetailViewSet(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'aidetail_form.html'
#     def get(self, request, format=None):
#         qs = AIDetail.objects.all()
#         serializer = AIDetailSerializer(qs, many =True)
#         return Response(serializer.data) #이렇게 해야 HTTPresponse로 감싸져서 나온다
        
#     def post(self, request):
#         serializer = AIDetailSerializer(data=[request.POST, request.FILES])
#         if serializer.is_valid():
#             # 추론서버에 요청
#             # 1. 외부 url 요청(AI 서버로)
#             files = request.FILES['photo']
#             upload = {'image': files}

#             url = 'http://192.168.1.141:8000/inference/'
#             res = requests.post(url, files = upload) # 요청한 결과 res에 받음

#             # 데이터 추가 저장
#             serializer.save(user=request.user, result=res.json()) #추가로 넣어주고 싶은 데이터를 키워드 인자로 넣어준다!
#         # return Response(serializer.data, status=201)
#         return redirect('profile-list')
        
# 함수로 따로 정의
# aidetail_list = AIDetailViewSet.as_view()
