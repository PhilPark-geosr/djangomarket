from django.contrib import admin
from .models import AIDetail, Task, InferenceModel
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # list_display =['id', 'post', 'message']
    # list_display_links =['message'] # 링크로 들어가고 싶은 곳에 지정
    # 지정필드값으로 필터링 옵션 제공
    # list_filter =['post']
    # 필터 쿼리를 날릴 수 있다
    # search_fields = ['message']
    pass

@admin.register(InferenceModel)
class InferenceModelAdmin(admin.ModelAdmin):
    # list_display =['id', 'post', 'message']
    # list_display_links =['message'] # 링크로 들어가고 싶은 곳에 지정
    # 지정필드값으로 필터링 옵션 제공
    # list_filter =['post']
    # 필터 쿼리를 날릴 수 있다
    # search_fields = ['message']
    pass
# Register your models here.
