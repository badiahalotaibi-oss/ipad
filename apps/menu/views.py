from types import SimpleNamespace

from django.http import Http404
from django.shortcuts import render

from .models import Category, MenuImage, MenuSettings


CATEGORY_LABELS = {
    'hot-coffee': ('القهوة', 'Coffee'),
    'coffee-of-the-day': ('قهوة اليوم', 'Coffee of the Day'),
    'drip-coffee': ('دريب كوفي', 'Drip Coffee'),
    'iced-coffee': ('قهوة باردة', 'Iced Coffee'),
    'cold-drinks': ('مشروبات باردة', 'Cold Drinks'),
    'dessert': ('الحلا', 'Sweet'),
    'croissant': ('الكرواسون', 'Croissant'),
    'breakfast': ('قائمة الفطور', 'Breakfast'),
}

HOME_CATEGORY_ORDER = [
    'hot-coffee',
    'coffee-of-the-day',
    'drip-coffee',
    'iced-coffee',
    'cold-drinks',
    'dessert',
    'croissant',
    'breakfast',
]

DEFAULT_CATEGORIES = [
    {'slug': slug, 'name_ar': names[0], 'name_en': names[1]}
    for slug, names in CATEGORY_LABELS.items()
]


def category_label(category):
    name_ar, name_en = CATEGORY_LABELS.get(
        category.slug,
        (category.name, category.description),
    )

    return {
        'slug': category.slug,
        'name_ar': name_ar,
        'name_en': name_en,
    }


def home(request):
    menu_settings = MenuSettings.objects.filter(is_active=True).first()
    categories_queryset = Category.objects.filter(is_active=True).order_by('display_order', 'name')
    category_order = {slug: index for index, slug in enumerate(HOME_CATEGORY_ORDER)}
    existing_category_slugs = set(
        Category.objects.filter(slug__in=HOME_CATEGORY_ORDER).values_list('slug', flat=True)
    )
    categories_by_slug = {
        category.slug: category_label(category)
        for category in categories_queryset
    }

    for default_category in DEFAULT_CATEGORIES:
        if default_category['slug'] not in existing_category_slugs:
            categories_by_slug.setdefault(default_category['slug'], default_category)

    categories = sorted(
        categories_by_slug.values(),
        key=lambda category: category_order.get(category['slug'], len(category_order)),
    )

    context = {
        'menu_settings': menu_settings,
        'categories': categories or DEFAULT_CATEGORIES,
    }

    return render(request, 'home.html', context)


def category_detail(request, slug):
    category = Category.objects.filter(slug=slug).first()

    if category and not category.is_active:
        raise Http404

    if category:
        menu_images = MenuImage.objects.filter(
            category=category,
            is_active=True
        ).order_by('display_order', 'created_at')
    elif slug in CATEGORY_LABELS:
        name_ar, name_en = CATEGORY_LABELS[slug]
        category = SimpleNamespace(slug=slug, name=name_ar, description=name_en)
        menu_images = MenuImage.objects.none()
    else:
        raise Http404

    context = {
        'category': category,
        'category_label': category_label(category),
        'menu_images': menu_images,
    }

    return render(request, 'category_detail.html', context)
