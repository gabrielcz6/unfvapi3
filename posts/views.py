# posts/views.py
from rest_framework import generics, permissions # new
from .models import Post
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly # new



class PostList(generics.ListCreateAPIView):
   queryset = Post.objects.all()
   permission_classes = (IsAuthorOrReadOnly,) # new
   serializer_class = PostSerializer
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
   permission_classes = (IsAuthorOrReadOnly,) # new
   queryset = Post.objects.all()
   serializer_class = PostSerializer
