from django.shortcuts import render, redirect
from django.http import Http404
from .models import Product


def index(request):
    cart = request.session.get('cart', [])

    products = Product.objects.filter(is_available=True)

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

            if item['quantity'] < product.stock:
                item['quantity'] += 1

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