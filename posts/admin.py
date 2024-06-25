from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from mptt.admin import DraggableMPTTAdmin

from posts.models import Post, Category, Comment


# Register your models here.

class ReplyInline(NestedStackedInline):
    model = Comment
    fields = ('author', 'body', 'is_reply', 'reply_to')
    extra = 0


class CommentInline(NestedStackedInline):
    model = Comment
    fields = ('author', 'body', 'is_reply', 'reply_to')
    extra = 0
    inlines = [ReplyInline]


@admin.register(Comment)
class CommentAdmin(NestedModelAdmin):
    list_display = ('author', 'post', 'created_time', 'is_reply')
    inlines = [CommentInline]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk','description',)
    inlines = [CommentInline]


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)
