# ِDjango
from django.contrib import admin
from django.utils.html import strip_tags
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from mptt.admin import DraggableMPTTAdmin

# local
from .models import Post, Category, Comment
from utils.mixins import CreatedUpdatedTimeAdminMixin

# third party
from ckeditor.widgets import CKEditorWidget
from modeltranslation.admin import TranslationAdmin


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
class CommentAdmin(CreatedUpdatedTimeAdminMixin, NestedModelAdmin):
    list_display = ('author', 'post', 'is_reply',
                    *CreatedUpdatedTimeAdminMixin.list_display)
    inlines = [CommentInline]
    readonly_fields = CreatedUpdatedTimeAdminMixin.readonly_fields


@admin.register(Post)
class PostAdmin(CreatedUpdatedTimeAdminMixin, TranslationAdmin):
    list_display = ('pk', 'title',
                    *CreatedUpdatedTimeAdminMixin.list_display)
    inlines = [CommentInline]
    readonly_fields = CreatedUpdatedTimeAdminMixin.readonly_fields


class CategoryAdmin(DraggableMPTTAdmin, TranslationAdmin):
    pass


admin.site.register(
    Category,
    CategoryAdmin,
    list_display=(
        'pk',
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'pk',
        'indented_title',
    ),
)
