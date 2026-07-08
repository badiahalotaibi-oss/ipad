from django.contrib import admin

from .models import MenuSettings, Category, MenuImage


@admin.register(MenuSettings)
class MenuSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "site_name",
        "subtitle",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "site_name",
        "subtitle",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("بيانات المنيو", {
            "fields": (
                "site_name",
                "subtitle",
                "logo",
                "is_active",
            )
        }),
        ("التواريخ", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


class MenuImageInline(admin.TabularInline):
    model = MenuImage
    extra = 1

    fields = (
        "title",
        "image",
        "alt_text",
        "price",
        "calories",
        "allergens",
        "display_order",
        "is_active",
    )

    ordering = (
        "display_order",
        "created_at",
    )


@admin.register(MenuImage)
class MenuImageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "title_en",
        "category",
        "price",
        "calories",
        "display_order",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "title",
        "title_en",
        "description",
        "allergens",
        "alt_text",
    )

    list_editable = (
        "price",
        "calories",
        "display_order",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "بيانات المنتج",
            {
                "fields": (
                    "category",
                    "title",
                    "title_en",
                    "description",
                    "image",
                    "alt_text",
                )
            },
        ),
        (
            "السعر والسعرات والحساسية",
            {
                "fields": (
                    "price",
                    "calories",
                    "allergens",
                )
            },
        ),
        (
            "الترتيب والظهور",
            {
                "fields": (
                    "display_order",
                    "is_active",
                )
            },
        ),
        (
            "التواريخ",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )