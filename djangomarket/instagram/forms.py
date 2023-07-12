from django import forms
from .models import Post
# from .models import AI
# 정규표현식
import re

# model명과 form 명을
# naming rule : {model명} + Form

'''
 Model Form 사용법
 1. class Meta 에 상속받을 모델명 기입
    model = {상속받을 모델}
    fields = ['원하는 필드명'] or '__all__'
'''
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        # 유효성 검사를 수행할 필드들
        fields= ['message', 'photo', 'tag_set', 'is_public']

    # 개별 필드에 대한 유효성 검사 로직 추가
    '''
    함수명 : clean_{필드명}
    '''
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            message = re.sub(r'[a-zA-Z]+', '', message) #영어가 있으면 없애버린다
        return message

# class AIForm(forms.ModelForm):
#     class Meta:
#         model = AI
#         fields = ['user','photo']
        