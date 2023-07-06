from django.db import models

# settings 불러 올때 이렇게 할것 이래야 우리가 정의한 settings를 오버라이드 함
from django.conf import settings

#TODO: 다시 볼것
from django.urls import reverse

# validator
from django.core.validators import MinLengthValidator


# Create your models here.
# for AI

# 그냥 기본모델로 추론 할 때 쓰임
class AI(models.Model):
    # upload to : settings.MEDIA_URL/instagram/post/%Y/%m/%d/ 폴더에 쌓임
    # 누가 추론했는지

    '''
    related name : {appname}_{modelname}_set
    ''' 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_ai_set")
    # 디비에는 파일이 저장된 경로가 들어감
    # TODO: 사진 저장 경로바꿀것
    photo = models.ImageField(blank= True, upload_to='ai/post/%Y/%m/%d') ## pillow 라이브러리가 설치되어야 있어야 함!
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    # result_url = models.TextField()
    result = models.JSONField()
    # URL reverse
    def get_absolute_url(self):
        return reverse("ai:ai_list")

    # qs 정렬 조건
    class Meta:
        ordering = ['-id']

class AIDetail(models.Model):
    # upload to : settings.MEDIA_URL/instagram/post/%Y/%m/%d/ 폴더에 쌓임

    '''
    related name : {appname}_{modelname}_set
    ''' 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_aidetail_set")
    
    # 어떤 카테고리 작업을 할건지.. 1개 카테고리에 N개 Post이 존재할 수 있으므로..
    task_category = models.ForeignKey('ai.Task', on_delete=models.CASCADE)

    # 어떤 모델을 사용할 것인지
    model_name = models.ForeignKey('ai.InferenceModel', on_delete=models.CASCADE)

    # 디비에는 파일이 저장된 경로가 들어감
    photo = models.ImageField(blank= True, upload_to='ai/detail//%Y/%m/%d') ## pillow 라이브러리가 설치되어야 있어야 함!
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    
    # 추론결과 넘어오는 필드
    result = models.JSONField()
    # URL reverse
    def get_absolute_url(self):
        return reverse("ai:aidetail_list")

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

    # 모델 명
    name = models.TextField()
    def __str__(self):
        # return f"Custom Post object create_at {self.created_at}"
        return self.name