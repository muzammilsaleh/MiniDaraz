from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product.stock < quantity:
        messages.warning(request, "Not enough stock available.")
        return redirect('product_detail', product_id=product.id)

    cart = get_user_cart(request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    messages.success(request, "Item added to cart.")
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = get_user_cart(request.user)
    cart_items = cart.items.select_related('product')
    total = cart.get_total()
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.warning(request, "Item not found.")
    return redirect('view_cart')

@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        try:
            new_qty = int(request.POST.get('quantity', 1))
            if 0 < new_qty <= item.product.stock:
                item.quantity = new_qty
                item.save()
                messages.success(request, "Quantity updated.")
            else:
                messages.warning(request, "Invalid quantity or insufficient stock.")
        except ValueError:
            messages.error(request, "Invalid input.")
    return redirect('view_cart')
@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product.stock < quantity:
        return redirect('product_detail', product_id=product.id)

    # Cart cleanup or creation
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()  # Clear previous cart

    # Add selected product
    CartItem.objects.create(cart=cart, product=product, quantity=quantity)

    return redirect('checkout')
