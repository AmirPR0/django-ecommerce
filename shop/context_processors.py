from .models import Category


def categories_processor(request):
    categories = Category.objects.all()

    return {
        'navbar_categories': categories
    }