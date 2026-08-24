from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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