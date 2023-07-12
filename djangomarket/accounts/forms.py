from django import forms
from .models import Profile

# 원래 LoginView에 기본으로 구현되어 있는 AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
# 정규표현식
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'zipcode']


class LoginForm(AuthenticationForm):
    # 원하는 필드 추가
    answer = forms.IntegerField(help_text='3 + 3 = ?')

    # 유효성 검사 로직 추가
    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        if answer !=6:
            raise forms.ValidationError('땡입니다')
        return answer


