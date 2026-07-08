from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.db import models


def category_image_upload_path(instance, filename):
    """
    هذه الدالة موجودة فقط حتى لا تتعطل ملفات migrations القديمة.
    الآن الصور الجديدة ترفع على Cloudinary.
    """
    slug = getattr(instance, "slug", "uncategorized") or "uncategorized"
    return f"menu/categories/{slug}/{filename}"


def menu_image_upload_path(instance, filename):
    """
    هذه الدالة موجودة فقط حتى لا تتعطل ملفات migrations القديمة.
    الآن الصور الجديدة ترفع على Cloudinary.
    """
    category = getattr(instance, "category", None)
    category_slug = getattr(category, "slug", "uncategorized") if category else "uncategorized"
    return f"menu/items/{category_slug}/{filename}"


def validate_image_size(image):
    """
    التحقق من حجم الصورة حتى لا يتم رفع صور ضخمة جدًا.
    الحد هنا 5MB.
    """
    max_size_mb = 5

    if image and hasattr(image, "size"):
        if image.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"حجم الصورة يجب ألا يتجاوز {max_size_mb}MB.")


class MenuSettings(models.Model):
    """
    إعدادات عامة للمنيو.
    نستخدمها للتحكم في اسم المحل، العنوان، والشعار من لوحة التحكم.
    """

    site_name = models.CharField(
        max_length=100,
        default="Digital Menu",
        verbose_name="اسم المنيو",
    )

    subtitle = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="وصف مختصر",
    )

    logo = CloudinaryField(
        folder="menu/logo",
        blank=True,
        null=True,
        validators=[validate_image_size],
        verbose_name="الشعار",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="مفعل",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    class Meta:
        verbose_name = "إعدادات المنيو"
        verbose_name_plural = "إعدادات المنيو"

    def __str__(self):
        return self.site_name


class Category(models.Model):
    """
    أقسام المنيو الرئيسية.
    مثال:
    فطور، قهوة، حلا، كرواسون، مشروبات باردة.
    """

    name = models.CharField(
        max_length=100,
        verbose_name="اسم القسم",
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        db_index=True,
        help_text="مثال: breakfast أو coffee أو dessert",
        verbose_name="الرابط المختصر",
    )

    description = models.TextField(
        blank=True,
        verbose_name="وصف القسم",
    )

    image = CloudinaryField(
        folder="menu/categories",
        blank=True,
        null=True,
        validators=[validate_image_size],
        verbose_name="صورة القسم",
    )

    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="ترتيب الظهور",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="إظهار القسم",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    class Meta:
        verbose_name = "قسم"
        verbose_name_plural = "الأقسام"
        ordering = ["display_order", "name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "display_order"]),
        ]

    def __str__(self):
        return self.name


class MenuImage(models.Model):
    """
    منتجات / صور المنيو داخل كل قسم.
    مثال:
    منتجات الفطور، مشروبات القهوة، منتجات الحلا.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="menu_images",
        verbose_name="القسم",
    )

    title = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="اسم المنتج بالعربي",
    )

    title_en = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="اسم المنتج بالإنجليزي",
    )

    description = models.TextField(
        blank=True,
        verbose_name="وصف المنتج",
    )

    image = CloudinaryField(
        folder="menu/items",
        validators=[validate_image_size],
        verbose_name="صورة المنتج / صورة المنيو",
    )

    alt_text = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="وصف الصورة",
        help_text="وصف مختصر للصورة لتحسين الوصول وتجربة المستخدم.",
    )

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="السعر",
    )

    calories = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="السعرات الحرارية",
        help_text="اكتب الرقم فقط، مثال: 581",
    )

    allergens = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="مسببات الحساسية",
        help_text="مثال: قمح / جلوتين، حليب / لاكتوز، بيض",
    )

    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="ترتيب المنتج",
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="إظهار المنتج",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الإنشاء",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث",
    )

    class Meta:
        verbose_name = "منتج منيو"
        verbose_name_plural = "منتجات المنيو"
        ordering = ["display_order", "created_at"]
        indexes = [
            models.Index(fields=["category", "is_active"]),
            models.Index(fields=["display_order"]),
        ]

    def __str__(self):
        if self.title and self.title_en:
            return f"{self.title} - {self.title_en}"

        if self.title:
            return self.title

        if self.title_en:
            return self.title_en

        return f"منتج منيو - {self.category.name}"