from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("signup/", views.SignUp.as_view()), # 이메일 회원가입
    path("login/", views.Login.as_view()), # 이메일 로그인
    path("login/refresh", TokenRefreshView.as_view()), # refresh token 발급
    path("logout/", views.Logout.as_view()), # 로그아웃
    path("list/", views.UserList.as_view()), # 유저 리스트 조회 (admin용)
]
