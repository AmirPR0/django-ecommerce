from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    # نام دسته‌بندی محصول
    name = models.CharField(max_length=100)

    # آدرس قابل استفاده برای URL دسته‌بندی
    slug = models.SlugField(unique=True)

    # تصویر دسته‌بندی
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    def __str__(self):
        # نمایش نام دسته‌بندی در پنل Admin
        return self.name


class Product(models.Model):
    # نام محصول
    name = models.CharField(max_length=200)

    # آدرس قابل استفاده در URL
    slug = models.SlugField(unique=True)

    # دسته‌بندی محصول
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )

    # توضیحات کامل محصول
    description = models.TextField()

    # توضیح کوتاه محصول
    short_description = models.CharField(
        max_length=300,
        blank=True
    )

    # قیمت محصول
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # تعداد موجودی محصول
    stock = models.PositiveIntegerField(default=0)

    # تصویر محصول
    image = models.ImageField(
        upload_to="products/"
    )

    # مشخص می‌کند محصول قابل فروش است یا نه
    is_available = models.BooleanField(default=True)

    # تاریخ ایجاد محصول
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # تاریخ آخرین بروزرسانی محصول
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ساخت Slug اولیه از روی نام محصول
        base_slug = slugify(self.name)

        # Slug اولیه را به عنوان Slug فعلی قرار می‌دهیم
        unique_slug = base_slug

        # شماره‌ای که در صورت تکراری بودن به Slug اضافه می‌شود
        counter = 2

        # بررسی می‌کنیم آیا این Slug قبلاً استفاده شده است یا نه
        while Product.objects.filter(
            slug=unique_slug
        ).exclude(pk=self.pk).exists():

            # در صورت تکراری بودن، شماره به انتهای Slug اضافه می‌شود
            unique_slug = f"{base_slug}-{counter}"

            # شماره برای تلاش بعدی افزایش پیدا می‌کند
            counter += 1

        # Slug نهایی را روی محصول قرار می‌دهیم
        self.slug = unique_slug

        # ذخیره محصول در دیتابیس
        super().save(*args, **kwargs)


class Order(models.Model):
    # کاربری که سفارش را ثبت کرده است
    # اگر کاربر حذف شود، خود سفارش باقی می‌ماند
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    # وضعیت‌های ممکن برای سفارش
    STATUS_CHOICES = [
        ('pending', 'Pending'),      # سفارش در انتظار پرداخت
        ('paid', 'Paid'),            # سفارش پرداخت شده
        ('cancelled', 'Cancelled'),  # سفارش لغو شده
    ]

    # مبلغ نهایی سفارش
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # وضعیت فعلی سفارش
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # تاریخ و زمان ایجاد سفارش
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # نمایش خواناتر سفارش در پنل Admin
        return f"Order #{self.id}"


class OrderItem(models.Model):
    # مشخص می‌کند این آیتم متعلق به کدام سفارش است
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    # محصولی که در این سفارش خریداری شده
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    # تعداد خریداری شده از محصول
    quantity = models.PositiveIntegerField()

    # قیمت محصول در زمان ثبت سفارش
    # تا اگر قیمت محصول بعداً تغییر کرد، سفارش قدیمی تغییر نکند
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        # نمایش نام محصول و تعداد آن در Admin
        return f"{self.product.name} x {self.quantity}"
