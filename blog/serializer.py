from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Post, Comment, Like, PostView


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'text', 'created_at', 'updated_at']
        read_only_fields = ['post', 'user']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author']

    def validate_title(self, title):
        if len(title) < 5:
            raise ValidationError("Sarlavha kamida 5 ta belgidan iborat bo'lsin")
        return title

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['likes_count'] = instance.likes.count()
        data['views_count'] = instance.views.count()
        return data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['post', 'user']


class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = ['id', 'post', 'user', 'updated_at']