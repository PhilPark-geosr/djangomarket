from django.db import models

# settings 불러 올때 이렇게 할것 이래야 우리가 정의한 settings를 오버라이드 함
from django.conf import settings

#TODO: 다시 볼것
from django.urls import reverse

# validator
from django.core.validators import MinLengthValidator


# Create your models here.
# for AI
class AI(models.Model):
    # upload to : settings.MEDIA_URL/instagram/post/%Y/%m/%d/ 폴더에 쌓임
    # 누가 추론했는지
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_inference_set")
    # 디비에는 파일이 저장된 경로가 들어감
    # TODO: 사진 저장 경로바꿀것
    photo = models.ImageField(blank= True, upload_to='ai/post/%Y/%m/%d') ## pillow 라이브러리가 설치되어야 있어야 함!
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)
    result_url = models.TextField()
    
    # URL reverse
    def get_absolute_url(self):
        return reverse("ai:ai_list")

    # qs 정렬 조건
    class Meta:
        ordering = ['-id']