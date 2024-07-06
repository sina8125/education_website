# local
from .models import Post, Category

# third party
from modeltranslation.translator import register, TranslationOptions


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Category)
class PostTranslationOptions(TranslationOptions):
    fields = ('name',)
