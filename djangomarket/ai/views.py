# Http Request, Response 관련
from django.http	import HttpRequest,	HttpResponse, Http404

# Models
from .models import  AI
from django.contrib.auth import get_user_model

# Forms
from .forms import AIForm

# render
from django.shortcuts import render, redirect, get_object_or_404
# 다른 웹서버에 자료 요청용
import requests

# CBV
from django.views.generic import ListView, DetailView
# import requests

# decorator
from django.contrib.auth.decorators	import login_required
# CBV에 입힐 데코레이터
from django.utils.decorators	import method_decorator
# 로그인 인증 관련
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.



def ai_new(request):

    if request.method =="POST":
        '''
        author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        # upload to : settings.MEDIA_URL/instagram/post/%Y/%m/%d/ 폴더에 쌓임
        # 디비에는 파일이 저장된 경로가 들어감
        photo = models.ImageField(blank= True, upload_to='instagram/post/%Y/%m/%d') ## pillow 라이브러리가 설치되어야 있어야 함!
        created_at= models.DateTimeField(auto_now_add =True)
        updated_at = models.DateTimeField(auto_now =True)
        result_url = models.TextField()
        '''
         #외부 url 요청 처리하는 로직
        # user모델 받아온다
        
        form = AIForm(request.POST, request.FILES)

        # print(form)
        # # print(request.data)
        if form.is_valid(): #유효성 검사 로직 수행

            User = get_user_model()
            current_user = User.objects.filter(pk=request.POST['user'])
            # print('user', current_user)

            files = request.FILES['photo']
            upload = {'image': files}

            # res = requests.post(' http://127.0.0.1:5000/image/', files = upload)
            url = 'http://192.168.1.141:8000/inference/'
            res = requests.post(url, files = upload)
            # print(res.json())
            # 모델 인스턴스 생성
            # print(request.POST)
            temp = AI(user = current_user.first() , photo = request.FILES['photo'], result_url = res.json()['result_image_url'] )
            # print(temp)
            # 모델결과 저장
            temp.save()
            
            # TODO: 요청결과 테이블로 볼 수 있도록 생성
            # return redirect('/instagram/ai/inference/')

            # url reverse
            return redirect(temp)
        
    else: #request.method == "GET"일경우 
        # 빈 폼 반환
        form = AIForm()
    # print(form)
    
    return render(request, 'ai/ai_form.html', {
        'form' : form,
    })


def ai_list(request):
    # print(request.GET)
    q = request.GET.get('q', '')
    if q:
        User = get_user_model()

        # 쿼리스트링으로 넘어온 유저로 검색
        current_user = get_object_or_404(User, username=q)
        # current_user = User.objects.filter(username=q).first()
        
        # 유저에 해당되는 모든 ai 결과들 쿼리
        qs = current_user.ai_inference_set.all()
        print(qs)
    # instagram/templates/instagram/post_list.html
    else:
        # 쿼리스트링으로 아무것도 안들어올 시 그냥 모두 검색
        qs = AI.objects.all()
        
    return render(request, 'ai/ai_list.html', {
        'ai_list' : qs,
        'q' : q,
    })