# Http Request, Response 관련
from django.http	import HttpRequest,	HttpResponse, Http404

# Models
from .models import Post, AI
from django.contrib.auth import get_user_model
# Forms
from .forms import PostForm, AIForm

# render
from django.shortcuts import render, redirect, get_object_or_404
# 다른 웹서버에 자료 요청용
import requests

# CBV
from django.views.generic import ListView, DetailView
# import requests


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
            return redirect('/instagram/ai/inference/')
        
            # return redirect('')
        
    else: #request.method == "GET"일경우 
        # 빈 폼 반환
        form = AIForm()
    # print(form)
    
    return render(request, 'instagram/ai_form.html', {
        'form' : form,
    })

def post_new(request):

    if request.method =="POST":
         #외부 url 요청 처리하는 로직
        # print(request.FILES['image'].name, type(request.FILES['image'].name))
        
        # print('요청전',request.FILES)
        
        # print('request 목록',request.url)
        # print('요청후',request.FILES)
        
        form = PostForm(request.POST, request.FILES)
        # print(form)
        # print(request.data)
        if form.is_valid(): #유효성 검사 로직 수행
            files = request.FILES['image']
            upload = {'image': files}

            # res = requests.post(' http://127.0.0.1:5000/image/', files = upload)
            url = 'http://192.168.1.141:8000/inference/'
            res = requests.post(url, files = upload)
            # print(res.text)
            # DB에 저장
            post = form.save()
            # redirect 
            # TODO: abolute url구현
            # return redirect(post)
            
            return redirect('/instagram/ai/inference/')
        
    else: #request.method == "GET"일경우 
        # 빈 폼 반환
        form = PostForm()
    # print(form)
    
    return render(request, 'instagram/post_form.html', {
        'form' : form,
    })
    
'''
form 내용 : 테이블 html 태그이므로, <table></table>로 감싸야 한다!

<tr><th><label for="id_message">Message:</label></th><td><textarea name="message" cols="40" rows="10" required id="id_message">
</textarea></td></tr>
<tr><th><label for="id_photo">Photo:</label></th><td><input type="file" name="photo" accept="image/*" id="id_photo"></td></tr>
<tr><th><label for="id_is_public">공개여부:</label></th><td><input type="checkbox" name="is_public" id="id_is_public"></td></tr>
'''


# CBV
post_list = ListView.as_view(model = Post, paginate_by =10)

# FBV
# def post_list(request):
#     qs = Post.objects.all()
#     print(request.GET)
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains = q)
#     # instagram/templates/instagram/post_list.html
#     return render(request, 'instagram/post_list.html', {
#         'post_list' : qs,
#         'q' : q,
#     })

# def post_detail(request, pk):
#     response = HttpResponse()
#     response.write("Hello World!")
#     return response


# CBV

'''
기본버전
DetailView에는 따로 안넘겨도 query string이 catpure되어 넘겨진다

path('<int:pk>/', views.post_detail),
여기서 pk가 인자로 알아서 넘어가서 queryset을 형성한다

'''
# 기본버전
'''
post_detail = DetailView.as_view(model = Post)

'''

# is_public = True인것만 볼 수 있게
'''
post_detail = DetailView.as_view(
    model = Post,
    queryset= Post.objects.filter(is_public =True)
)
'''

class PostDetailView(DetailView):
    model = Post
    # queryset = Post.objects.filter(is_pubic = True)
    
    # DetailView를 상속받아 재정의
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:  # 현재 로그인 한 유저의 인스턴스
            qs = qs.filter(is_public = True) # 로그인 안한 유저들은 is_public = True만 볼 수 있도록
        return qs
post_detail = PostDetailView.as_view()

# FBV
# def post_detail(request, pk): # 두번째 인자 이름은 urls.py의 path('<int:pk>/', views.post_detail), 의 capture 된 문자열과 정확하게 일치해야 한다!
#     # try:
#     #     post = Post.objects.get(pk = pk)
#     # except:
#     #     raise Http404

#     # 위와 같은 로직
#     post = get_object_or_404(Post, pk = pk)

#     return render(request, 'instagram/post_detail.html', {
#         'post' : post,
#     })


    

def ai_list(request):
    # print(request.GET)
    q = request.GET.get('q', '')
    if q:
        User = get_user_model()
        current_user = User.objects.filter(username=q).first()
        qs = current_user.ai_set.all()
        print(qs)
    # instagram/templates/instagram/post_list.html
    else:
        qs = AI.objects.all()
        
    return render(request, 'instagram/ai_list.html', {
        'ai_list' : qs,
        'q' : q,
    })