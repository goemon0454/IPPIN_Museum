from operator import and_
from functools import reduce
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.timezone import make_aware
import datetime
from django.contrib.auth import get_user_model
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ItemForm
from .models import Item

# カスタムユーザー取得
User = get_user_model()

# いいね追加、削除
def like(request):
    item = get_object_or_404(Item, id=request.POST.get('item_id'))
    if request.user.like_items.filter(id=item.id).exists():
        request.user.like_items.remove(item)
        item.like_users.remove(request.user)
        item.likes-=1
        print(item.create_at)
        print(item.update_at)
        item.save()
    else:    
        request.user.like_items.add(item)
        item.like_users.add(request.user)
        item.likes+=1
        item.save()
    # 現在のページにリダイレクト
    return redirect(request.META['HTTP_REFERER'])

# 新着ソート
class NewItemListView(ListView):
    model = Item
    template_name = "items/new_items.html"
    context_object_name = "new_items_list"
    paginate_by = 24

    def get_queryset(self):
        return Item.objects.order_by('update_at').reverse()[:240]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログインユーザーのlike_itemsをリストで取得→いいね済み判定{like_items(ユーザーのいいねした商品数)の方がlike_users(商品のいいねされた数)よりも処理が少ないと判断}
        user_id = self.request.user.id
        like_items = User.objects.filter(id=user_id).values_list("like_items", flat=True)
        context["like_items"] = like_items
        return context


# 検索＋新着
class SearchNew(ListView):
    template_name = "search/new_result.html"
    context_object_name = "new_result_list"
    paginate_by = 24

    def get_queryset(self):
        exit_str = False
        for x in self.request.GET.get('q', ''):
            if x != " " and x != "　":
                exit_str = True
        # 検索窓がスペースのみでない場合
        if exit_str == True:
            if self.request.GET.get('q', ''):
                params = self.parse_search_params(self.request.GET['q'])
                query = reduce(and_, [Q(item_name__icontains=p) | Q(comment__icontains=p) | Q(description__icontains=p) for p in params])
                return Item.objects.filter(query).order_by('update_at').reverse()[:240]
        else:
            return Item.objects.order_by('update_at').reverse()[:240]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        like_items = User.objects.filter(id=user_id).values_list("like_items", flat=True)
        context["like_items"] = like_items
        context["query"] = self.request.GET.get('q', '')
        return context
    
    def parse_search_params(self, words: str):
        search_words = words.replace(' ', ' ').split()
        return search_words

# いいね順ソート
class PopularItemListView(ListView):
    model = Item
    template_name = "items/popular_items.html"
    context_object_name = "popular_items_list"
    paginate_by = 24
    
    def get_queryset(self):
        return Item.objects.order_by('likes', 'update_at').reverse()[:240]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        like_items = User.objects.filter(id=user_id).values_list("like_items", flat=True)
        context["like_items"] = like_items
        return context
    
# 検索＋いいね
class SearchPopular(ListView):
    template_name = "search/popular_result.html"
    context_object_name = "popular_result_list"
    paginate_by = 24

    def get_queryset(self):
        exit_str = False
        for x in self.request.GET.get('q', ''):
            if x != " " and x != "　":
                exit_str = True
        # 検索窓がスペースのみでない場合
        if exit_str == True:
            if self.request.GET.get('q', ''):
                params = self.parse_search_params(self.request.GET['q'])
                query = reduce(and_, [Q(item_name__icontains=p) | Q(comment__icontains=p) | Q(description__icontains=p) for p in params])
                return Item.objects.filter(query).order_by('likes', 'update_at').reverse()[:240]
        else:
            return Item.objects.order_by('likes', 'update_at').reverse()[:240]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        like_items = User.objects.filter(id=user_id).values_list("like_items", flat=True)
        context["like_items"] = like_items
        context["query"] = self.request.GET.get('q', '')
        return context
    
    def parse_search_params(self, words: str):
        search_words = words.replace(' ', ' ').split()
        return search_words

# ランダム表示（ページネーションは無し）
class RandomItemListView(ListView):
    model = Item
    template_name = "items/random_items.html"
    context_object_name = "random_items_list"

    def get_queryset(self):
        return Item.objects.order_by('?')[:48]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        like_items = User.objects.filter(id=user_id).values_list("like_items", flat=True)
        context["like_items"] = like_items
        return context

# 検索＋ランダム
class SearchRandom(ListView):
    template_name = "search/random_result.html"
    context_object_name = "random_result_list"

    def get_queryset(self):
        exit_str = False
        for x in self.request.GET.get('q', ''):
            if x != " " and x != "　":
                exit_str = True
        # 検索窓がスペースのみでない場合
        if exit_str == True:
            if self.request.GET.get('q', ''):
                params = self.parse_search_params(self.request.GET['q'])
                query = reduce(and_, [Q(item_name__icontains=p) | Q(comment__icontains=p) | Q(description__icontains=p) for p in params])
                return Item.objects.filter(query).order_by('?')[:48]
        else:
            return Item.objects.order_by('?')[:48]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        like_items = User.objects.filter(id=user_id).values_list("like_items", flat=True)
        context["like_items"] = like_items
        context["query"] = self.request.GET.get('q', '')
        return context
    
    def parse_search_params(self, words: str):
        search_words = words.replace(' ', ' ').split()
        return search_words

# 新規投稿アップロード処理
def post_item(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                item = Item()
                item.thumbnail = request.FILES.get('thumbnail', "images/thumbnails/no_image.png")
                item.comment = request.POST['comment']
                item.item_name = request.POST['item_name']
                item.description = request.POST['description']
                item.update_at = make_aware(datetime.datetime.now())
                item.user = request.user
                item.save()
                return redirect('items:new-items-list')
        else:
            form = ItemForm()
        return render(request, 'items/post_item.html', {'form': form})
    else:
        return redirect("accounts:login")

# 投稿編集
def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user.is_authenticated and request.user == item.user:
        # 更新完了、マイページへ飛ばす
        if request.method == "POST":
            form = ItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                item.thumbnail = request.FILES.get('thumbnail', item.thumbnail)
                item.comment = request.POST['comment']
                item.item_name = request.POST['item_name']
                item.description = request.POST['description']
                item.update_at = make_aware(datetime.datetime.now())
                item.user = request.user
                item.save()
                return redirect(reverse("accounts:mypage-post-items", kwargs={"pk": request.user.id}))
        # 更新ページ訪問時、現在値を表示
        else:
            form = ItemForm(instance=item)
            return render(request, "items/update_item.html", {"form": form})
    else:
        return redirect("accounts:login")

# 投稿削除
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user.is_authenticated and request.user == item.user:
        if request.method == "POST":
            item.delete()
            return redirect(reverse("accounts:mypage-post-items", kwargs={"pk": request.user.id}))
        else:
            return render(request, "items/delete_item.html", {"item": item})
    else:
        return redirect("accounts:login")

