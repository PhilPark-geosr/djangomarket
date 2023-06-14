from django.db import models

# settings 불러 올때 이렇게 할것
from django.conf import settings

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
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

    # qs 정렬 조건
    class Meta:
        ordering = ['-id']

class Comment(models.Model):
    post = models.ForeignKey('instagram.Post', on_delete=models.CASCADE) # 실제 db에는 post_id 필드가 생성됨
    message = models.TextField()
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    class Meta:
        ordering = ['-id']