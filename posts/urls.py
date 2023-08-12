# posts/urls.py
from django.urls import path
from .views import PostList, PostDetail, UserList, UserDetail # new




urlpatterns = [
path("users/", UserList.as_view()), # new
path("users/<int:pk>/", UserDetail.as_view()), # new
path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
path("", PostList.as_view(), name="post_list"),
]