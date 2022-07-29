from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)

from posts.models import Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(ModelViewSet):
    """Публикации пользователей."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    """Группы публикаций по теме."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny, )


class CommentViewSet(ModelViewSet):
    """Комментарии к публикации."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, )

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user,
                        post=post)


class FollowViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """Подписки на авторов."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username', 'user__username', )

    def get_queryset(self):
        user = self.request.user
        new_queryset = user.follower.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
