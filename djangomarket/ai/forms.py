from django import forms
from .models import AI, AIDetail, InferenceModel

# model명과 form 명을
# naming rule : {model명} + Form

'''
 Model Form 사용법
 1. class Meta 에 상속받을 모델명 기입
    model = {상속받을 모델}
    fields = ['원하는 필드명'] or '__all__'
'''

class AIForm(forms.ModelForm):
    class Meta:
        model = AI
        fields = ['user','photo']
        

# 기본 하나의 모델에 있는 필드만 표출하고 싶을 경우
# class AIDetailForm(forms.ModelForm):
#     class Meta:
#         model = AIDetail
#         fields = ['user','photo', 'task_category', 'model_name']


# 외부 모델 필드 참조하고 싶을때
class AIDetailForm(forms.ModelForm):

    # 다른 모델 참조해서 필드에 넣고 싶을때
    inference_model_name = forms.ModelChoiceField(
        queryset=InferenceModel.objects.all(),
        label='Inference Model Name'
    )

    class Meta:
        model = AIDetail
        fields = ['user', 'photo', 'task_category', 'inference_model_name']

# class AIDetailForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         task_category = kwargs.pop('task_category', None)
#         super(AIDetailForm, self).__init__(*args, **kwargs)
#         if task_category:
#             self.fields['inference_model_name'].queryset = InferenceModel.objects.filter(task=task_category)

#     inference_model_name = forms.ModelChoiceField(
#         queryset=InferenceModel.objects.none(),
#         label='Inference Model Name'
#     )

#     class Meta:
#         model = AIDetail
#         fields = ['user', 'photo', 'task_category', 'inference_model_name']
