from django.utils.translation import get_language


def translate_field(instance, field_name):
    current_language = get_language()
    field_name_translated = f"{field_name}_en" if current_language.lower() != 'fa-ir' else field_name
    return getattr(instance, field_name_translated) or ""
