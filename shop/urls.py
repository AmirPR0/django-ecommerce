from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home_page'),
    path('<slug:slug>', views.product_details_view, name='product_details'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove-from-cart/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/add/<slug:slug>/', views.add_to_cart, name='add_quantity'),
    path('cart/decrease/<slug:slug>/', views.decrease_quantity, name='decrease_quantity'),
    # مسیر صفحه Checkout
    path('checkout/', views.checkout_view, name='checkout'),
    # صفحه موفقیت ثبت سفارش
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),

    # path('clear-cart/', views.clear_cart),
]