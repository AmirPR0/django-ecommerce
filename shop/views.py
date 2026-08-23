from django.shortcuts import render, redirect
from django.http import Http404
from .models import Product


products = {
    "iphon 17 pro max": {
        'slug': 'iphon-17-pro-max',
        'image': 'iphon_17_pro_max.jpg',
        'description': 'Latest Iphon Smart Phone.',
        'des': '512GB Orang',
        'price': '1200.0'
    },
    "samsung s25 ultra": {
        'slug': 'samsung-s25-ultra',
        'image': 'Samsung_s25_ultra.jpg',
        'description': 'Latest Samsung Smart Phone. Thats use AI.',
        'des': '512GB black',
        'price': '1400.0'
    },
    "xiaomi poco x7 pro": {
        'slug': 'xiaomi-poco-x7-pro',
        'image': 'Xiaomi_poco_x7_pro.jpg',
        'description': 'Latest Xiaomi Smart Phone.',
        'des': '256GB black',
        'price': '750.0'
    },
    "samsung A56": {
        'slug': 'samsung-A56',
        'image': 'Samsung_A56.png',
        'description': 'The best mid-range Samsung phone.',
        'des': '256GB white',
        'price': '600.0'
    },
    "honor 400": {
        'slug': 'honor-400',
        'image': 'Honor_400.png',
        'description': 'Latest Honor Smart Phone.',
        'des': '256GB white',
        'price': '520.0'
    },
    "xiaomi 17 pro max": {
        'slug': 'xiaomi-17-pro-max',
        'image': 'xiaomi-17-pro-max.jpg',
        'description': 'The best xiaomi smart phone.',
        'des': '256GB black',
        'price': '1000.0'
    }
}


def index(request):
    cart = request.session.get('cart', [])

    products_from_db = Product.objects.filter(is_available=True)

    return render(request, 'shop/index.html', {
        'products': products_from_db,
        'caller_view': 'home',
        'cart': cart
    })


def product_details_view(request, slug):
    item = slug.replace('-', ' ')
    if item in products:
        cart = request.session.get('cart', [])
        # محصولات مرتبط بدون محصول فعلی
        related_products = {k: v for k, v in products.items() if k != item}

        return render(request, 'shop/product_details.html', {
            'product': item,
            'details': products[item],
            'related_products': related_products,
            'caller_view': 'details',
            'cart': cart,
        })
    raise Http404


def add_to_cart(request, slug):
    item_name = slug.replace('-', ' ')
    if item_name not in products:
        raise Http404

    # گرفتن سبد خرید از session
    cart = request.session.get('cart', [])

    # مطمئن شدن که همه آیتم‌های قدیمی quantity دارن
    for item in cart:
        if 'quantity' not in item:
            item['quantity'] = 1

    # بررسی اینکه آیتم قبلاً اضافه شده یا نه
    for item in cart:
        if item['slug'] == slug:
            item['quantity'] += 1
            break
    else:
        # اگر آیتم جدید بود، به سبد اضافه می‌کنیم
        cart.append({
            'name': item_name,
            'price': products[item_name]['price'],
            'slug': slug,
            'image': products[item_name]['image'],
            'des': products[item_name]['des'],
            'quantity': 1
        })
    # ذخیره مجدد سبد در session
    request.session['cart'] = cart

    return redirect('cart_view')


def cart_view(request):
    cart = request.session.get('cart', [])
    total = sum([float(item['price']) * int(item.get('quantity', 1))
                for item in cart])

    # دریافت مقدار دلیوری از فرم
    delivery_fee = float(request.GET.get('shipping', 5))  # پیش‌فرض 5 یورو

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
            else:
                cart.remove(item)
            break

    request.session['cart'] = cart
    return redirect('cart_view')


def remove_from_cart(request, slug):
    cart = request.session.get('cart', [])

    cart = [item for item in cart if item['slug'] != slug]

    request.session['cart'] = cart

    return redirect('cart_view')


def clear_cart(request):
    request.session.flush()
    return redirect('home_page')

# اجرای این آدرس
# http://localhost:8000/clear-cart/
