from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Address, Order, OrderItem
from .forms import AddressForm
from cart.models import Cart

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('checkout')  
    else:
        form = AddressForm()
    return render(request, 'orders/add_address.html', {'form': form})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product')
    addresses = Address.objects.filter(user=request.user)
    total = cart.get_total()

    address_form = AddressForm()

    if request.method == 'POST':
        # check if new address form is submitted
        if 'full_name' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                new_address = address_form.save(commit=False)
                new_address.user = request.user
                new_address.save()
                messages.success(request, "New address added.")
                return redirect('checkout')

        else:
            address_id = request.POST.get('address')
            try:
                address = Address.objects.get(id=address_id, user=request.user)
            except Address.DoesNotExist:
                messages.error(request, "Please select a valid address.")
                return redirect('checkout')

            # Place order
            order = Order.objects.create(user=request.user, total_amount=total)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart.items.all().delete()
            messages.success(request, "Your order has been placed successfully!")
            return redirect('user_orders')

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'addresses': addresses,
        'total': total,
        'address_form': address_form
    })

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
