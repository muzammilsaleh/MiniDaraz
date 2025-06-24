from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem

@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        return redirect('cart_view')

    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(user=request.user, total_amount=total_amount)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    cart.items.all().delete()  # clear cart

    return redirect('order_detail', order_id=order.id)

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})
