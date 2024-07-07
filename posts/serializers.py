# local
from .models import Comment, Post, Category
from accounts.serializer import ProfileSerializer

# third party
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    solar_show_date = serializers.SerializerMethodField()
    show_date = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('pk', 'author', 'is_reply', 'available', 'body', 'show_date', 'solar_show_date', 'child')

    def get_child(self, obj):
        child = Comment.objects.filter(reply_to=obj.pk, available=True)
        if child:
            return CommentSerializer(child, many=True).data
        return None

    def get_author(self, obj):
        return str(obj.author)

    def get_solar_show_date(self, obj):
        return obj.solar_show_date

    def get_show_date(self, obj):
        return obj.show_date


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('pk', 'name', 'slug', 'parent')

    def get_parent(self, obj):
        if obj.parent:
            return CategorySerializer(obj.parent).data
        return None


class PostListSerializer(serializers.ModelSerializer):
    created_user = ProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'slug', 'thumbnail', 'is_premium', 'created_user', 'category', 'description')
