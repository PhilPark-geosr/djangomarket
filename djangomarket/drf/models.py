from django.db import models

# settings 불러 올때 이렇게 할것 이래야 우리가 정의한 settings를 오버라이드 함
from django.conf import settings

#TODO: 다시 볼것
from django.urls import reverse

# validator
from django.core.validators import MinLengthValidator


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="drf_post_set")
    message = models.TextField() #최소 10글자 유효성 검사 로직
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    is_public = models.BooleanField(default = False, db_index=True)

    # admin의 제목 바꾸고 싶을때
    def __str__(self):
        # return f"Custom Post object create_at {self.created_at}"
        return self.message
    # user defined 함수 지정할 수 있음, 단 인자 없어야 함!
    # def message_length(self):
    #     return len(self.message)
    # message_length.short_description = "메세지 글자수" # 노출될 필드명

    ''' URL Reverse 구현 꼭 모델에 구현해 놓아야 함!!'''
    # def get_absolute_url(self):
    #     return reverse("instagram:post_detail", args= [self.pk])
    
    # qs 정렬 조건
    class Meta:
        ordering = ['-id']


#------------------------------- for AI ----------------------------------#

class AIDetail(models.Model):
    # upload to : settings.MEDIA_URL/instagram/post/%Y/%m/%d/ 폴더에 쌓임

    '''
    related name : {appname}_{modelname}_set
    ''' 
  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="drf_aidetail_set")
    
    # 어떤 카테고리 작업을 할건지.. 1개 카테고리에 N개 Post이 존재할 수 있으므로..
    task_category = models.ForeignKey('drf.Task', on_delete=models.CASCADE, related_name="drf_aidetail_set")

    # 어떤 모델을 사용할 것인지
    # model_name = models.ForeignKey('ai.InferenceModel', on_delete=models.CASCADE)

    # 디비에는 파일이 저장된 경로가 들어감
    photo = models.ImageField(blank= True, upload_to='drf/ai/detail//%Y/%m/%d') ## pillow 라이브러리가 설치되어야 있어야 함!
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    
    # 추론결과 넘어오는 필드
    result = models.JSONField()
    # URL reverse
    # def get_absolute_url(self):
    #     return reverse("ai:aidetail_list")

    # qs 정렬 조건
    class Meta:
        ordering = ['-id']


class Task(models.Model):
    # Task 이름
    name = models.TextField()
    def __str__(self):
        # return f"Custom Post object create_at {self.created_at}"
        return self.name
    
    
class InferenceModel(models.Model):
    
    #TODO: 테이블 설계 바꾸기
    # task = models.ForeignKey('ai.Task', on_delete=models.CASCADE)

    # 모델 명
    task = models.ForeignKey('drf.Task', on_delete=models.CASCADE )
    name = models.TextField()
    def __str__(self):
        # return f"Custom Post object create_at {self.created_at}"
        return self.name

