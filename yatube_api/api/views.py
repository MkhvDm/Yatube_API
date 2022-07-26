from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from posts.models import Post, Group, Comment, Follow
from .permissions import ReadOnly, IsAuthor

from .serializers import (CommentSerializer, PostSerializer,
                          GroupSerializer, FollowSerializer)

User = get_user_model()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (AllowAny, )
    permission_classes = (IsAuthenticated | ReadOnly, IsAuthor, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated | ReadOnly, IsAuthor, )

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user,
                        post=post)


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        follow = User.following(user=user)
        return follow

    def perform_create(self, serializer):
        following = get_object_or_404(User, username=self.kwargs.get('username'))
        # post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(user=self.request.user,
                        following=following)
