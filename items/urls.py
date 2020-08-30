from django.urls import path
from . import views

app_name = "items"

urlpatterns = [
    path("", views.NewItemListView.as_view(), name="new-items-list"),
    path("popular-items/", views.PopularItemListView.as_view(), name="popular-items-list"),
    path("random-items/", views.RandomItemListView.as_view(), name="random-items-list"),
    path("search-new-items/", views.SearchNew.as_view(), name="search-new-items-list"),
    path("search-popular-items/", views.SearchPopular.as_view(), name="search-popular-items-list"),
    path("search-random-items/", views.SearchRandom.as_view(), name="search-random-items-list"),
    path("post-item/", views.post_item, name="post-item"),
    path("update-item/<int:item_id>", views.update_item, name="update-item"),
    path("delete-item/<int:item_id>", views.delete_item, name="delete-item"),
    path("like/", views.like, name="like"),
]
