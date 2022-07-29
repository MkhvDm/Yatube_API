from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    following = SlugRelatedField(
        slug_field='username',
        read_only=False,
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following', )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following', ),
                message='Вы уже подписаны на этого пользователя!'
            )
        ]

    def validate_following(self, value):
        """Rejects self-following."""
        user = self.context.get('request').user
        if value == user:
            raise serializers.ValidationError('Нельзя подписать на себя!')
        return value
