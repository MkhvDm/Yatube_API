from django.contrib.auth import get_user_model
from posts.models import Comment, Follow, Group, Post
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

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
        # read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(slug_field='username',
                                 read_only=False,
                                 queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following', )

    def validate_following(self, value):
        user = self.context.get('request').user
        if value == user:
            raise serializers.ValidationError('Нельзя подписать на себя!')
        if user.follower.filter(following=value):
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя!'
            )
        return value
