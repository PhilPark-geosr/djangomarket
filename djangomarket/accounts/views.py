from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# decorator
from django.contrib.auth.decorators	import login_required


# 로그인 인증 관련
from django.contrib.auth.mixins import LoginRequiredMixin

# CBV
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView

# model
from .models import Profile
from django.contrib.auth import get_user_model, login as auth_login #절대 auth.models의 User모델을 얻어오면 안됨

User = get_user_model()
# form
from .forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm

# settings
from django.conf import settings


# Create your views here.

#----------------------- detail view ---------------------------------#
#FBV
# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')

#CBV
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

profile = ProfileView.as_view()

#----------------------- update view ---------------------------------#

# FBV
@login_required
def profile_edit(request):

    # user에 프로필 정보가 없는 경우 None으로 처리하며 넘긴다
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method =="POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():

            profile = form.save(commit=False)
            # 데이터 추가
            profile.user = request.user
            profile.save()


            # success url
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile) 
    return render(request, 'accounts/profile_form.html', {
        'form' : form,
    })

#CBV
# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = Profile
#     form_class = ProfileForm

# profile_edit = ProfileUpdateView.as_view()

#----------------------- signup, logout view ---------------------------------#


# FBV
# def signup(request):
#     pass

# CBV
# 기본 : 회원기압 이후에 로그인 화면으로 감
# signup = CreateView.as_view(
#     model = User,
#     form_class = UserCreationForm,
#     success_url = settings.LOGIN_URL,
#     template_name = 'accounts/signup_form.html',
# )

# 회원가입하자마자 로그인 하고 싶을때 -> 단순 as_view로만 안됨!
# 상속받아서 멤버함수 추가 구현해야됨
class SignupView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'accounts/signup_form.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        user = self.object
        auth_login(self.request, user)
        return response
    
signup = SignupView.as_view()


def logout(request):
    pass