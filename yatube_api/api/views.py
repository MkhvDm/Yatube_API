from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from posts.models import Post
# from .permissions import IsAuthor

from .serializers import CommentSerializer, PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (AllowAny, )
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
