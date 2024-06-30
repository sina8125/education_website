from django import template
from django.utils.translation import get_language

register = template.Library()


class GetTranslatedFieldNode(template.Node):
    def __init__(self, instance, field_name):
        self.instance = template.Variable(instance)
        self.field_name = field_name

    def render(self, context):
        instance = self.instance.resolve(context)
        current_language = get_language()
        field_name_translated = f"{self.field_name}_en" if current_language.lower() != 'fa-ir' else self.field_name
        return getattr(instance, field_name_translated) or ""


@register.tag
def translate_field(parser, token):
    try:
        tag_name, instance, field_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.split_contents()[0]} tag requires exactly two arguments"
        )
    return GetTranslatedFieldNode(instance, field_name)
