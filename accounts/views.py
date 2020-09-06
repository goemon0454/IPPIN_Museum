from django import forms
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import SignupForm
from items.models import Item

# カスタムユーザー取得
User = get_user_model()

# アカウント登録
def signup(request):
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            username = signup_form.cleaned_data.get("username")
            password = signup_form.cleaned_data.get("password1")
            user = User.objects.create_user(username, password)
            user.save()
            # ユーザー認証、セッション管理
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('items:new-items-list')
    else:
        signup_form = SignupForm()
    return render(request, "accounts/signup.html", {"form": signup_form})

# ログイン
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    # バリデーション
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            raise forms.ValidationError("正しいアカウント名を入力してください")
        if not user.check_password(password):
            raise forms.ValidationError("正しいパスワードを入力してください")

# ログアウト
class UserLogoutView(LogoutView):
    template_name = "accounts/logout.html"

# マイページ
class MypageView(DetailView):
    model = User
    template_name = "accounts/mypage.html"
    context_object_name = "account_detail"
    

# マイページ：投稿したIPPIN
class MypagePostItem(DetailView):
    model = User
    template_name = "accounts/my_posts.html"
    context_object_name = "account_posts_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        post_items = Item.objects.filter(user=user_id).order_by('update_at').reverse()
        # ページネーション
        page_num = self.request.GET.get('page')
        pagenator = Paginator(post_items,24)
        try:
            page = pagenator.page(page_num)
        except PageNotAnInteger:
            page = pagenator.page(1)
        except EmptyPage:
            page = pagenator.page(pagenator.num_pages)
        context["page_obj"] = page
        context["is_paginated"] = page.has_other_pages
        context["user_id"] = user_id
        context["post_items"] = page.object_list
        # いいね判定
        user_id = self.request.user.id
        like_items = User.objects.filter(id=user_id).values_list("like_items", flat=True)
        context["like_items"] = like_items
        return context

# マイページ：いいねしたIPPIN
class MypageLikeItem(DetailView):
    model = User
    template_name = "accounts/my_likes.html"
    context_object_name = "account_likes_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('pk')
        my_like_items = User.objects.get(id=user_id).like_items.all().order_by('update_at').reverse()
        # ページネーション
        page_num = self.request.GET.get('p')
        pagenator = Paginator(my_like_items,24)
        try:
            page = pagenator.page(page_num)
        except PageNotAnInteger:
            page = pagenator.page(1)
        except EmptyPage:
            page = pagenator.page(pagenator.num_pages)
        context["page_obj"] = page
        context["is_paginated"] = page.has_other_pages
        context["user_id"] = user_id
        context["my_like_items"] = page.object_list
        # いいね判定
        user_id = self.request.user.id
        like_items = User.objects.filter(id=user_id).values_list("like_items", flat=True)
        context["like_items"] = like_items
        return context
    
