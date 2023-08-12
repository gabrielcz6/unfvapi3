# posts/views.py
from rest_framework import generics, permissions # new
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly # new
from django.contrib.auth import get_user_model # new
from .serializers import PostSerializer, UserSerializer # new
from rest_framework import viewsets # new
from rest_framework.permissions import IsAdminUser # new


class PostList(generics.ListCreateAPIView):
   queryset = Post.objects.all()
   permission_classes = (IsAuthorOrReadOnly,) # new
   serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
   permission_classes = (IsAuthorOrReadOnly,) # new
   queryset = Post.objects.all()
   serializer_class = PostSerializer

class UserList(generics.ListCreateAPIView): # new
   queryset = get_user_model().objects.all()
   serializer_class = UserSerializer
class UserDetail(generics.RetrieveUpdateDestroyAPIView): # new
   queryset = get_user_model().objects.all()
   serializer_class = UserSerializer