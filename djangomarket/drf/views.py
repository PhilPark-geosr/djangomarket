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

# parser : swagger에서 image upload 인식을 위함
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser,FileUploadParser

# wwagger api관련
from drf_yasg.utils import swagger_auto_schema
# import Model
from .models import Post, AIDetail

# Serializer
from .serializers import PostSerializer, AIDetailSerializer

# renderer 지정
from rest_framework.renderers import TemplateHTMLRenderer
# 다른 웹서버에 자료 요청용
import requests

# authentication and permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadonly

# filtering & Ordering
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # permission
    permission_classes = [IsAuthenticated, IsAuthorOrReadonly] #접근을 위해서는 로그인이 무조건 되어야 함을 지정해줌
    
    # filtering & Ordering
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['message'] #DB where 조건절 지정

    def perform_create(self, serializer):
        #FIXME: 인증이 되어있다는 가정하에 author를 지정 --> authentication_classes 지정!
        ip = self.request.META['REMOTE_ADDR']
        author = self.request.user
        serializer.save(author=author, ip = ip)

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
    parser_classes = (MultiPartParser,) ## swagger api에서 이미지 업로드 인식
    # def list(self, request):
    #     pass
    # def create(self, request):
    #     pass
    
    # create 함수 재정의 실제 create함수 호출될때 perform_create함수 호출
    def perform_create(self, serializer):
        files = self.request.FILES['photo']
        upload = {'image': files}
        
        url = 'http://192.168.1.141:8000/inference/'
        res = requests.post(url, files = upload) # 요청한 결과 res에 받음
        # 데이터 추가 저장
        serializer.save(user=self.request.user, result=res.json())

    # update시 수행되는 로직
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    # destory시 수행되는 로직
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    
    # action 추가로직 구현
    # @swagger_auto_schema(operation_description='Upload file...',)
    # @action(detail=False, methods=['post'])
    # def set_content(self, request):
    #     serializer = AIDetailSerializer(data=request.data)
    #     # print("request.POST",request.POST)
    #     if serializer.is_valid():

    #         # 추론서버에 데이터 요청
    #         files = request.FILES['photo']
    #         upload = {'image': files}

    #         url = 'http://192.168.1.141:8000/inference/'
    #         res = requests.post(url, files = upload) # 요청한 결과 res에 받음

    #         # 데이터 추가 저장
    #         serializer.save(user=request.user, result=res.json()) #추가로 넣어주고 싶은 데이터를 키워드 인자로 넣어준다!
    #         # print('savecomplete')
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

    # CBV에서 실제 요청이 올때마다 항상 소출되는 함수
    def dispatch(self, request, *args, **kwargs):
        print(f"request.body : {request.body}") #TODO: logger 사용
        print(f"request.POST : {request.POST}")
        return super().dispatch(request, *args, **kwargs)

class AIDetailViewSet2(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'aidetail_form.html'
    parser_classes = (MultiPartParser,FormParser, FileUploadParser)# image upload
    
    def get(self, request, format=None):
        qs = AIDetail.objects.all()
        serializer = AIDetailSerializer(qs, many =True)
        return Response(serializer.data) #이렇게 해야 HTTPresponse로 감싸져서 나온다
        
    def post(self, request):
        serializer = AIDetailSerializer(data=request.data)
        if serializer.is_valid():
            # 추론서버에 요청
            # 1. 외부 url 요청(AI 서버로)
            files = request.FILES['photo']
            upload = {'image': files}
            
            url = 'http://192.168.1.141:8000/inference/'
            res = requests.post(url, files = upload) # 요청한 결과 res에 받음

            # 데이터 추가 저장
            serializer.save(user=request.user, result=res.json()) #추가로 넣어주고 싶은 데이터를 키워드 인자로 넣어준다!
        return Response(serializer.data, status=201)
        # return redirect('profile-list')
        
# 함수로 따로 정의
# aidetail_list = AIDetailViewSet.as_view()
