from django import forms
from .models import Post, AI

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
        fields = '__all__'
        

class AIForm(forms.ModelForm):
    class Meta:
        model = AI
        fields = ['photo']
        