from django.db import models

# settings 불러 올때 이렇게 할것 이래야 우리가 정의한 settings를 오버라이드 함
from django.conf import settings

#TODO: 다시 볼것
from django.urls import reverse

# validator
from django.core.validators import MinLengthValidator


# Create your models here.
# for AI
# class AI(models.Model):
#     # upload to : settings.MEDIA_URL/instagram/post/%Y/%m/%d/ 폴더에 쌓임
#     # 누가 추론했는지
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     # 디비에는 파일이 저장된 경로가 들어감
#     # TODO: 사진 저장 경로바꿀것
#     photo = models.ImageField(blank= True, upload_to='ai/post/%Y/%m/%d') ## pillow 라이브러리가 설치되어야 있어야 함!
#     created_at= models.DateTimeField(auto_now_add =True)
#     updated_at = models.DateTimeField(auto_now =True)
#     result_url = models.TextField()
    
#     # URL reverse
#     def get_absolute_url(self):
#         return reverse("instagram:ai_list")

#     # qs 정렬 조건
#     class Meta:
#         ordering = ['-id']
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(validators=[MinLengthValidator(10)]) #최소 10글자 유효성 검사 로직
    #message = models.TextField(validators=[MinLengthValidator(10)]) #최소 10글자 유효성 검사 로직
    
    # tag set
    # many to many 에서는 blank = True로 두는게 편함
    # 이유 : 포스팅에 태그를 작성 안할수도 있으므로..!
    tag_set= models.ManyToManyField('Tag', blank = True)
    # upload to : settings.MEDIA_URL/instagram/post/%Y/%m/%d/ 폴더에 쌓임
    # 디비에는 파일이 저장된 경로가 들어감
    photo = models.ImageField(blank= True, upload_to='instagram/post/%Y/%m/%d') ## pillow 라이브러리가 설치되어야 있어야 함!
    is_public = models.BooleanField(default=False, verbose_name="공개여부")
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    # admin의 제목 바꾸고 싶을때
    def __str__(self):
        # return f"Custom Post object create_at {self.created_at}"
        return self.message
    # user defined 함수 지정할 수 있음, 단 인자 없어야 함!
    # def message_length(self):
    #     return len(self.message)
    # message_length.short_description = "메세지 글자수" # 노출될 필드명

    ''' URL Reverse 구현 꼭 모델에 구현해 놓아야 함!!'''
    def get_absolute_url(self):
        return reverse("instagram:post_detail", args= [self.pk])
    
    # qs 정렬 조건
    class Meta:
        ordering = ['-id']

class Comment(models.Model):
    post = models.ForeignKey('instagram.Post', on_delete=models.CASCADE,
                             # 댓글을 쓸 수 있는 posting 항목 제한
                             # Post 모델의 is_public 이 True인 것만 댓글을 달 수 있도록 하겠다!
                             limit_choices_to={'is_pulic' : True}) # 실제 db에는 post_id 필드가 생성됨
    message = models.TextField()
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    class Meta:
        ordering = ['-id']

#
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # post_set = 

     # admin의 제목 바꾸고 싶을때
    def __str__(self):
        return self.name