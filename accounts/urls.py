from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="sign-up"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    # pk:移動したいマイページのユーザーid
    path("mypage/<int:pk>", views.MypageView.as_view(), name="mypage"),
    path("mypage/<int:pk>/post-items", views.MypagePostItem.as_view(), name="mypage-post-items"),
    path("mypage/<int:pk>/like-items", views.MypageLikeItem.as_view(), name="mypage-like-items"),
]