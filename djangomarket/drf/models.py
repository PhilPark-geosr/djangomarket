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

