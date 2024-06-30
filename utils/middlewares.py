from django.utils import translation


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang_code = request.GET.get('lang')
        if lang_code:
            translation.activate(lang_code)
            request.LANGUAGE_CODE = lang_code
        response = self.get_response(request)
        return response
