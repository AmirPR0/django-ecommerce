from django.shortcuts import render, redirect
from django.http import Http404
from .models import Product


def index(request):
    cart = request.session.get('cart', [])

    products_from_db = Product.objects.filter(is_available=True)

    return render(request, 'shop/index.html', {
        'products': products_from_db,
        'caller_view': 'home',
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
        is_available=True
    ).exclude(
        id=product.id
    )

    return render(request, 'shop/product_details.html', {
        'product': product,
        'related_products': related_products,
        'caller_view': 'details',
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
            item['quantity'] += 1
            break
    else:
        cart.append({
            'name': product.name,
            'price': str(product.price),
            'slug': product.slug,
            'image': product.image.url,
            'des': product.short_description,
            'quantity': 1
        })

    request.session['cart'] = cart

    return redirect('cart_view')


def cart_view(request):
    cart = request.session.get('cart', [])

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
            else:
                cart.remove(item)
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

    return redirect('cart_view')


def clear_cart(request):
    request.session.flush()

    return redirect('home_page')