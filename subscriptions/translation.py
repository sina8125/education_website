# local
from .models import Package

# third party
from modeltranslation.translator import register, TranslationOptions


@register(Package)
class PackageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
