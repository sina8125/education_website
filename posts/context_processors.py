from .models import Category


def category_processor(request):
    categories = Category.objects.filter(level=0)
    if not categories.exists():
        categories = None
    return {
        'categories': categories
    }
