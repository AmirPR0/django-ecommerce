from django.shortcuts import render, redirect
from django.http import Http404
from django.db import transaction
from django.contrib import messages

from .models import Category, Product, Order, OrderItem


def index(request):
    # دریافت دسته‌بندی‌های فروشگاه
    categories = Category.objects.all()

    # دریافت سبد خرید از Session
    cart = request.session.get('cart', [])

    # نمایش صفحه Home
    return render(request, 'shop/index.html', {
        'categories': categories,
        'caller_view': 'home',
        'cart': cart
    })


def category_products(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        raise Http404

    cart = request.session.get('cart', [])

    categories = Category.objects.all()

    products = Product.objects.filter(
        category=category,
        is_available=True
    )

    for product in products:
        product_in_cart = next(
            (item for item in cart if item['slug'] == product.slug),
            None
        )

        quantity_in_cart = (
            product_in_cart.get('quantity', 0)
            if product_in_cart
            else 0
        )

        product.remaining_stock = max(
            product.stock - quantity_in_cart,
            0
        )

    return render(request, 'shop/index.html', {
        'products': products,
        'category': category,
        'categories': categories,
        'caller_view': 'category',
        'cart': cart
    })


def product_details_view(request, slug):
    try:
        product = Product.objects.get(
            slug=slug,
            is_available=True
        )
    except Product.DoesNotExist:
        raise Http404

    cart = request.session.get('cart', [])

    related_products = Product.objects.filter(
        category=product.category, is_available=True).exclude(id=product.id)

    return render(request, 'shop/product_details.html', {
        'product': product,
        'related_products': related_products,
        'caller_view': 'details',
        'cart': cart,
    })

def search_products(request):
    # دریافت عبارت جستجو از Query String
    # مثال: /search/?q=Samsung
    query = request.GET.get('q', '').strip()

    # در حالت عادی هیچ محصولی نمایش داده نمی‌شود
    products = Product.objects.none()

    # اگر کاربر عبارتی وارد کرده باشد، محصولات را جستجو می‌کنیم
    if query:
        products = Product.objects.filter(
            name__icontains=query,
            is_available=True
        )

    # دریافت سبد خرید از Session
    cart = request.session.get('cart', [])

    # نمایش صفحه نتایج جستجو
    return render(request, 'shop/search_results.html', {
        'products': products,
        'query': query,
        'caller_view': 'search',
        'cart': cart,
    })


def add_to_cart(request, slug):
    try:
        product = Product.objects.get(
            slug=slug,
            is_available=True
        )
    except Product.DoesNotExist:
        raise Http404

    cart = request.session.get('cart', [])

    for item in cart:
        if 'quantity' not in item:
            item['quantity'] = 1

    for item in cart:
        if item['slug'] == product.slug:
            if item['quantity'] < product.stock:
                item['quantity'] += 1
                messages.success(request, 'Product added to cart.')
            else:
                messages.error(request, 'Not enough stock available.')

            break

    else:
        if product.stock > 0:
            cart.append({
                'name': product.name,
                'price': str(product.price),
                'slug': product.slug,
                'image': product.image.url,
                'des': product.short_description,
                'quantity': 1
            })

            messages.success(request, 'Product added to cart.')
        else:
            messages.error(request, 'Product is out of stock.')

    request.session['cart'] = cart

    return redirect('cart_view')


def cart_view(request):
    cart = request.session.get('cart', [])

    for item in cart:
        try:
            product = Product.objects.get(
                slug=item['slug'],
                is_available=True
            )

            item['stock'] = product.stock

        except Product.DoesNotExist:
            item['stock'] = 0

    total = sum(
        float(item['price']) * int(item.get('quantity', 1))
        for item in cart
    )

    delivery_fee = float(request.GET.get('shipping', 5))

    total_with_delivery = total + delivery_fee

    return render(request, 'shop/cart.html', {
        'cart': cart,
        'total': total,
        'delivery_fee': delivery_fee,
        'total_with_delivery': total_with_delivery
    })


def decrease_quantity(request, slug):
    cart = request.session.get('cart', [])

    for item in cart:
        if item['slug'] == slug:
            if item['quantity'] > 1:
                item['quantity'] -= 1
                messages.error(request, 'Product quantity decreased.')
            else:
                cart.remove(item)
                messages.error(request, 'Product removed from cart.')

            break

    request.session['cart'] = cart

    return redirect('cart_view')


def remove_from_cart(request, slug):
    cart = request.session.get('cart', [])

    cart = [
        item for item in cart
        if item['slug'] != slug
    ]

    request.session['cart'] = cart

    messages.error(request, 'Product removed from cart.')

    return redirect('cart_view')


def clear_cart(request):
    request.session.flush()

    return redirect('home_page')


def checkout_view(request):
    # دریافت سبد خرید از Session
    cart = request.session.get('cart', [])

    # اگر سبد خرید خالی باشد، کاربر را به صفحه سبد خرید برمی‌گردانیم
    if not cart:
        return redirect('cart_view')

    # محاسبه مبلغ کل محصولات
    total = sum(
        float(item['price']) * int(item.get('quantity', 1))
        for item in cart
    )

    # هزینه ارسال
    delivery_fee = float(request.GET.get('shipping', 5))

    # مبلغ نهایی سفارش
    total_with_delivery = total + delivery_fee

    # اگر کاربر روی Place Order کلیک کرده باشد
    if request.method == 'POST':

        # تمام عملیات ثبت سفارش را به صورت یک تراکنش انجام می‌دهیم
        with transaction.atomic():

            # بررسی موجودی تمام محصولات قبل از ثبت سفارش
            for item in cart:
                product = Product.objects.get(
                    slug=item['slug']
                )

                # اگر موجودی کافی نباشد، سفارش ثبت نمی‌شود
                if product.stock < item['quantity']:
                    return redirect('cart_view')

            # ساخت سفارش جدید
            order = Order.objects.create(
                total_price=total_with_delivery
            )

            # ساخت آیتم‌های سفارش و کاهش موجودی
            for item in cart:
                product = Product.objects.get(
                    slug=item['slug']
                )

                # ایجاد OrderItem
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price']
                )

                # کاهش موجودی محصول
                product.stock -= item['quantity']
                product.save()

            # بعد از ثبت موفق سفارش، سبد خرید خالی می‌شود
            request.session['cart'] = []

            # نمایش پیام موفقیت ثبت سفارش
            messages.success(request, 'Order placed successfully.')

            # بعد از ثبت موفق سفارش، کاربر را به صفحه موفقیت سفارش می‌فرستیم
            return redirect('order_success', order_id=order.id)

    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'total': total,
        'delivery_fee': delivery_fee,
        'total_with_delivery': total_with_delivery
    })


def order_success(request, order_id):
    # پیدا کردن سفارش ثبت شده
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise Http404

    # نمایش صفحه موفقیت سفارش
    return render(request, 'shop/order_success.html', {
        'order': order
    })


def order_detail(request, order_id):
    # پیدا کردن سفارش بر اساس ID
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise Http404

    # دریافت آیتم‌های مربوط به این سفارش
    order_items = order.items.all()

    # نمایش صفحه جزئیات سفارش
    return render(request, 'shop/order_detail.html', {
        'order': order,
        'order_items': order_items,
    })


def order_list(request):
    # دریافت تمام سفارش‌های ثبت شده
    orders = Order.objects.all().order_by('-created_at')

    # نمایش صفحه سفارش‌ها
    return render(request, 'shop/orders.html', {
        'orders': orders,
    })