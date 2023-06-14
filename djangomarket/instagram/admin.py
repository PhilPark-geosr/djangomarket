from django.contrib import admin
from .models import Post, Comment
from django.utils.safestring import mark_safe
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # admin 페이지에서 표출할 필드 지정
    # list_display에 들어갈수 있는 항목 : Post모델의 필드 이름 or 사용자 정의 함수들..
    list_display =['id', 'photo_tag', 'message', 'is_public','created_at', 'updated_at', 'message_length']
    list_display_links =['message', 'created_at'] # 링크로 들어가고 싶은 곳에 지정
    # 지정필드값으로 필터링 옵션 제공
    list_filter =['created_at', 'is_public']
    # 필터 쿼리를 날릴 수 있다
    search_fields = ['message']

    # 특별히 admin단에서만 보고싶은 필드 or 메소드 정의
    # 두번째 인자로 정의된 모델이 넘어온다
    def message_length(self, model):
        return len(model.message)
    message_length.short_description = "메세지 글자수" # 노출될 필드명

    def photo_tag(self, model):
        if model.photo: #필드가 있을경우
            #mark safe : 원래는 이미지 안나오게 막아놓는데, mark_safe로 감싸면 html태그가 변환되서 나옴
            return mark_safe(f'<img src = "{model.photo.url}" style = "width: 50px;"/>')
        return None    


# Post model    
'''
class Post(models.Model):
    message = models.TextField()
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
'''

@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    # admin 페이지에서 표출할 필드 지정
    # list_display에 들어갈수 있는 항목 : Post모델의 필드 이름 or 사용자 정의 함수들..
    list_display =['id', 'post', 'message']
    list_display_links =['message'] # 링크로 들어가고 싶은 곳에 지정
    # 지정필드값으로 필터링 옵션 제공
    list_filter =['post']
    # 필터 쿼리를 날릴 수 있다
    search_fields = ['message']

    # 특별히 admin단에서만 보고싶은 필드 or 메소드 정의
    
'''
class Comment(models.Model):
    post = models.ForeignKey('instagram.Post', on_delete=models.CASCADE) # 실제 db에는 post_id 필드가 생성됨
    message = models.TextField()
    created_at= models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    class Meta:
        ordering = ['-id']
'''