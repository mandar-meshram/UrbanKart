from django.shortcuts import render, redirect
from Products.models import Products
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from Registration.models import Registration
from django import messages


def add_to_cart(request):
    if not request.session.get('user_id'):
        return redirect('login_user')

    user = Registration.objects.get(id=request.session['user_id'])
    product_id = request.POST.get('product_id')
    product = Products.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(user=user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
        item.save()

    return redirect('view_cart')    


def view_cart(request):
    if not request.session.get('user_id'):
        return redirect('login_user')

    user = Registration.objects.get(id=request.session['user_id'])
    cart = Cart.objects.filter(user=user).first()

    if not cart:
        return render(request, 'view_cart.html', {'cart_items': [], 'grand_total': 0})

    cart_items = cart.items.select_related('product')
    grand_total = sum(item.total_price() for item in cart_items)

    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })

def update_cart_item(request, item_id):
    if not request.session.get('user_id'):
        return redirect('login_user')
    
    user = Registration.objects.get(id=request.session['user_id'])
    cart = Cart.objects.filter(user=user).first()
    item = CartItem.objects.get(id=item_id, cart=cart)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        item.quantity = quantity
        item.save()
        messages.success(request, "Cart item updated successfully.")
        return redirect('view_cart')

    return render(request, 'update_cart_item.html', {'item': item})