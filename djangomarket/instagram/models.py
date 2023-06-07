from django.db import models

# Create your models here.
class Post(models.Model):
    message = models.TextField()
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

    