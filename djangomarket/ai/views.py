# Http Request, Response 관련
from django.http	import HttpRequest,	HttpResponse, Http404

# Models
from .models import  AI, AIDetail, Task
from django.db import models
from django.contrib.auth import get_user_model

# Forms
from .forms import AIForm, AIDetailForm

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
        # 폼 생성
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
            res = requests.post(url, files = upload) # 요청한 결과 res에 받음
            # print(res.json())
            # 모델 인스턴스 생성
            # print(request.POST)
            # temp = AI(user = current_user.first() , photo = request.FILES['photo'], result_url = res.json()['result_image_url'] )
            
            temp = AI(user = current_user.first() , photo = request.FILES['photo'], result = res.json())
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

def aidetail_new(request):
    if request.method =="POST":
         
        form = AIDetailForm(request.POST, request.FILES)

        # print(form)
        # # print(request.data)
        if form.is_valid(): #유효성 검사 로직 수행
            # user모델 받아온다
            # User = get_user_model()
            # current_user = User.objects.filter(pk=request.POST['user'])
            # print('user', current_user)


            # 1. 외부 url 요청(AI 서버로)
            files = request.FILES['photo']
            upload = {'image': files}

            # res = requests.post(' http://127.0.0.1:5000/image/', files = upload)
            url = 'http://192.168.1.141:8000/inference/'
            res = requests.post(url, files = upload) # 요청한 결과 res에 받음
            # print(res.json())
            # 모델 인스턴스 생성
            # print(request.POST)
             
            # 2. form save
            '''
            form.save() 하면 내부적으로 model instance를 반환해줌
            form.save()에는 내부적으로 유효성 검사 통과한 clean_data가 넘어감
            ''' 
            aidetail = form.save(commit=False) #commit False로 해야 추가적인 정보를 저장할 수 있음
            # print("aidetail", aidetail)
            # 3. 데이터 추가
            '''
            API 요청해서 받은 결과를 모델인스턴스에 추가함
            '''
            aidetail.result = res.json()
            aidetail.user = request.user # 유저정보 입력
            aidetail.save() #이래야 최종적으로 DB에 저장됨

            # 4. go success url 
            return redirect(aidetail) # url reverse
            # return redirect('http://127.0.0.1:8000/ai/inference/detail/')
    else: #request.method == "GET"일경우 
        # 빈 폼 반환
        form = AIDetailForm()

        # form = AIDetailForm(task_category=my_task_category)
    # print(form)
    
    return render(request, 'ai/aidetail_form.html', {
        'form' : form,
    })

# 기존 코드
# def ai_list(request):
#     # print(request.GET)
    
#     q = request.GET.get('q', '')
#     if q:
#         User = get_user_model()

#         # 쿼리스트링으로 넘어온 유저로 검색
#         current_user = get_object_or_404(User, username=q)
#         # current_user = User.objects.filter(username=q).first()
        
#         # 유저에 해당되는 모든 ai 결과들 쿼리
#         qs = current_user.ai_ai_set.all()
#         print(qs)
#     # instagram/templates/instagram/post_list.html
#     else:
#         # 쿼리스트링으로 아무것도 안들어올 시 그냥 모두 검색
#         qs = AI.objects.all()
        
#     return render(request, 'ai/ai_list.html', {
#         'ai_list' : qs,
#         'q' : q,
#     })


# 개선코드
@login_required #로그인 필수
def ai_list(request):
    # GET 인자로 넘어온 것 확인
    # print(request.GET)
    
    # 로그인된 유저 확인
    # print('로그인된 유저', request.user )

    # 검색 기능 구현
    # 사용모델로 검색
    q = request.GET.get('q', '')
    if q:
        User = get_user_model()

        # 쿼리스트링으로 넘어온 유저로 검색
        current_user = get_object_or_404(User, username=q)
        # current_user = User.objects.filter(username=q).first()
        
        # 유저에 해당되는 모든 ai 결과들 쿼리
        qs = current_user.ai_ai_set.all()
        print(qs)
    # instagram/templates/instagram/post_list.html
    else:
        # 쿼리스트링으로 아무것도 안들어올 시 유저이름으로 그냥 모두 검색
        qs = AI.objects.filter(user = request.user)
        
    return render(request, 'ai/ai_list.html', {
        'ai_list' : qs,
        'q' : q,
    })

@login_required
def aidetail_list(request):
    # print(request.GET)

    q = request.GET.get('q')
    
    #FIXME: 다른 필드 넣어서 확인
    # if q:
    #     qs = AIDetail.objects.all()
    #     qs = qs.filter(
    #         models.Q(task_category__icontains=q) |
    #         models.Q(user__icontains=q)
    #     )

    if q:
        User = get_user_model()

        # 쿼리스트링으로 넘어온 유저로 검색
        current_user = get_object_or_404(User, username=q)
        # current_user = User.objects.filter(username=q).first()
        
        # 유저에 해당되는 모든 ai 결과들 쿼리
        qs = current_user.ai_aidetail_set.all()
        # print(qs)
    # instagram/templates/instagram/post_list.html
    else:
        # 쿼리스트링으로 아무것도 안들어올 시 그냥 모두 검색
        qs = AIDetail.objects.all()
        
    return render(request, 'ai/aidetail_list.html', {
        'aidetail_list' : qs,
        'q' : q,
    })


# @login_required
# def aidetail_list(request):
#     # print(request.GET)

#     # 추론한 모델 태스크로 검색
#     q = request.GET.get('q', '')
#     if q:
#         #TODO: 문자열 포함결과로 검색 구현
#         # task = Task.objects.filter(name__icontains = 'In')

#         # 쿼리스트링으로 넘어온 태스크 카테고리로 검색 
#         task = get_object_or_404(Task, name=q)
        
#         # 태스크에 해당되는 모든 ai 결과들 쿼리
#         qs = task.ai_aidetail_set.all()
#         # print(qs)
    
#     # instagram/templates/instagram/post_list.html
#     else:
#         # 쿼리스트링으로 아무것도 안들어올 시 유저가 요청한 추론 내역이 다 보임
#         qs = AIDetail.objects.filter(user = request.user)
        
#     return render(request, 'ai/aidetail_list.html', {
#         'aidetail_list' : qs,
#         'q' : q,
#     })

# --------------------------Detail View ---------------------------#

# @login_required
class AIDetailDetailView(DetailView):
    model = AIDetail
    # queryset = Post.objects.filter(is_pubic = True)
    
    # DetailView를 상속받아 재정의
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     if not self.request.user.is_authenticated:  # 현재 로그인 한 유저의 인스턴스
    #         qs = qs.filter(is_public = True) # 로그인 안한 유저들은 is_public = True만 볼 수 있도록
    #     return qs

aidetail_detail = AIDetailDetailView.as_view()