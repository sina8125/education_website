from rest_framework import serializers

from posts.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    solar_show_date = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('pk', 'author', 'is_reply', 'available', 'body', 'solar_show_date', 'child')

    def get_child(self, obj):
        child = Comment.objects.filter(reply_to=obj.pk, available=True)
        if child:
            return CommentSerializer(child, many=True).data
        return None

    def get_author(self, obj):
        return str(obj.author)

    def get_solar_show_date(self, obj):
        return obj.solar_show_date
