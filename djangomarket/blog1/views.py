from django.shortcuts import render
from .models import Post

# Create your views here.
def post_list(request):
    qs = Post.objects.all() # 쿼리문 뭔지 입력

    # render(request, html경로, {전달할 데이터})
    # html경로 : templates/{app이름}/{html이름}
    return render(request, 'blog1/post_list.html', {
        'post_list' : qs,

    })