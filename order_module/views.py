from ast import Delete
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, reverse
from .models import *
from cart_module.models import Cart, CartItem
from  account_module.models import User
# Create your views here.


def order_save(request):
    order = Order.objects.create(user=request.user)
    cart = Cart.objects.get(user=request.user)
    order.save()
    totalprice = 0
    for item in cart.items.all():
        orderItem, created = OrderItem.objects.update_or_create(
            order=order, product=item.product, price=item.price, quantity=item.quantity)
        order.order_items.add(orderItem)
        totalprice += item.price * item.quantity

    order.address = request.POST['address']
    order.total_price = totalprice
    order.address_second = request.POST['second_address']
    order.postal_code = request.POST['postalcode']
    order.province = request.POST['province']
    order.city = request.POST['city']
    order.save()

    #clear cart and card items
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
   
    return redirect('../go-to-gateway/' + str(order.id))

   
    

def order_create(request):

    # return redirect(reverse('payment:process'))

    #profile = get_object_or_404(User, user=request.user)
    cart = Cart.objects.get(user=request.user)
    
    return render(request, 'order_module/order_list.html', {'cart': cart  , 'user' : request.user})