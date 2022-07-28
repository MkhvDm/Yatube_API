from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, Comment, Follow
from .permissions import IsAuthorOrReadOnly

from .serializers import (CommentSerializer, PostSerializer,
                          GroupSerializer, FollowSerializer)

User = get_user_model()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (AllowAny, )
    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny, )


class CommentViewSet(ModelViewSet):
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


class FollowViewSet(ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        # new_queryset = Follow.objects.filter(user=user.pk)
        new_queryset = user.follower.all()
        return new_queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print('\nser data:', serializer.initial_data)
        following = get_object_or_404(
            User, username=serializer.initial_data.get('following')
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        # TODO check existing follow & not user
        serializer.save(user=self.request.user)


# class FollowViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
#     serializer_class = FollowSerializer
#     permission_classes = (IsAuthenticated,)


