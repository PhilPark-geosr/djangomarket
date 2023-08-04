## 데이터 직렬화 관련 
# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, AIDetail, Task, InferenceModel

# 내장 유저모델 임포트할때 반드시 이렇게!
from django.contrib.auth import get_user_model

'''
기존 필드를 가공하여 1:N or N:M 관계에 있는 필드의 정보를 보여주고 싶을때
방법 1 : serializers.ReadOonlyField 사용
'''
class PostSerializer(serializers.ModelSerializer):

    # 별도로 참조 처리해서 보여지고 싶은 필드 작성 
    username = serializers.ReadOnlyField(source = 'author.username')
    user_email =  serializers.ReadOnlyField(source = 'author.email')

    class Meta:
        model = Post
        # fields = "__all__" # 모든 필드 리스트 직렬화 해서 보여줌
        fields = [
            # 원래 모델에 ㅇ
            'pk',
            'message',
            'created_at',
            'updated_at',
            'is_public',
            'ip', # ReadOnly로 걸고 싶으면.. Model 클래스의 ip field에 editable = False 지정!

            # 원래 모델에는 없는 필드이나 모델의 필드를 가공하여(1:N for N:M 관계 활용), 
            # serializers.ReadOnlyField에 추가하여 보여질 수 있게 함
            'username',
            'user_email',

        ] #원하는 필드 리스트만 직렬화 해서 보여줌


'''
기존 필드를 가공하여 1:N or N:M 관계에 있는 필드의 정보를 보여주고 싶을때
방법 2 : serializers 중첩 사용
'''
# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['username', 'email']

# class PostSerializer(serializers.ModelSerializer):

#     author = AuthorSerializer()

#     class Meta:
#         model = Post
#         # fields = "__all__" # 모든 필드 리스트 직렬화 해서 보여줌
#         fields = [
#             # 해당 모델에만 있는 정보들
#             'pk',
#             'message',
#             'created_at',
#             'updated_at',
#             'is_public',

#             # 1:N or N:M관계 있는 필드들
#             'author', 

#         ] #원하는 필드 리스트만 직렬화 해서 보여줌

#---------------------------------- for AI -------------------------------------------#
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


#TODO: pk나오도록 조치

class AIDetailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source = 'user.username')
    
    class Meta:
        model = AIDetail
        read_only_fields = ('result','username')
        fields = ['pk','photo', 'username','result']