from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from .models import Category, Product, Order, OrderItem


# مدیریت Product در پنل Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Slug توسط Django ساخته می‌شود و نیازی به نمایش آن در فرم نیست
    exclude = ('slug',)

    def get_changeform_initial_data(self, request):
        # دریافت اطلاعات اولیه فرم Product
        initial = super().get_changeform_initial_data(request)

        # دریافت شناسه Category از URL
        category_id = request.GET.get('category')

        # اگر Category از صفحه Category ارسال شده باشد
        if category_id:
            initial['category'] = category_id

        return initial


# مدیریت Category در پنل Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # فیلدهای فقط خواندنی که توسط متدهای پایین ساخته می‌شوند
    readonly_fields = (
        'add_product_button',
        'products_list',
    )

    # نمایش دکمه Add Product
    @admin.display(description='Add Product')
    def add_product_button(self, obj):
        # اگر Category هنوز ذخیره نشده باشد
        if not obj or not obj.pk:
            return 'Save the category first.'

        # ساخت URL صفحه اضافه کردن Product
        url = reverse('admin:shop_product_add')

        # ارسال شناسه Category به صفحه Product
        url = f'{url}?category={obj.pk}'

        # ساخت دکمه
        return format_html(
            '<a href="{}" class="button">Add Product</a>',
            url,
        )

    # نمایش محصولات این Category
    @admin.display(description='Products')
    def products_list(self, obj):
        # اگر Category هنوز ذخیره نشده باشد
        if not obj or not obj.pk:
            return '-'

        # دریافت محصولات مربوط به این Category
        products = obj.products.all().order_by('name')

        # اگر محصولی وجود نداشته باشد
        if not products:
            return 'No products'

        # ساخت لینک برای هر محصول
        return format_html_join(
            format_html('<br>'),
            '<a href="{}">{}</a>',
            (
                (
                    reverse(
                        'admin:shop_product_change',
                        args=[product.pk]
                    ),
                    product.name,
                )
                for product in products
            ),
        )


# ثبت مدل‌های سفارش در پنل Admin
admin.site.register(Order)
admin.site.register(OrderItem)