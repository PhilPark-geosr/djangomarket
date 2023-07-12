from django.contrib.auth.views import LoginView, LogoutView

# form
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm

from django.urls import path
from . import views

urlpatterns = [
    #login logout signup
    path('login/', LoginView.as_view(
        # form_class = AuthenticationForm, #기본으로 구현되어있음 이 폼을 보여주는 것임
        form_class = LoginForm, #user defined form
        template_name ="accounts/login_form.html"), 
        name='login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('signup/', views.signup, name='signup'),
    # profile
    path('profile/', views.profile, name = 'profile'),
    path('profile/edit/', views.profile_edit, name = 'profile_edit'),
    
    
]
