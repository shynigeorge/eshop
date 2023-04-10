import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from cart.models import Items, Cart
from cart.views import cart_id
from homepage.models import Product
from order.models import Order, Itemorder, Profile


def checkout(request):
    cart_items = None
    tot = 0

    ct = Cart.objects.get(cart_id=cart_id(request))
    cart_items = Items.objects.filter(cart=ct, active=True)
    for i in cart_items:
        tot += (i.products.price * i.quantity)

    userprofile = Profile.objects.filter(user=request.user).first()
    return render(request, 'checkout.html', {'item': cart_items, 'totalprice': tot, 'userprofile': userprofile})


def placeorder(request):
    if request.method == 'POST':

        currentuser = User.objects.filter(id=request.user.id).first()
        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.mobileno = request.POST.get('mobileno')
            userprofile.address = request.POST.get('address')
            userprofile.country = request.POST.get('country')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.zipcode = request.POST.get('zipcode')
            userprofile.save()

    neworder = Order()
    neworder.user = request.user
    neworder.fname = request.POST.get('fname')
    neworder.lname = request.POST.get('lname')
    neworder.email = request.POST.get('email')
    neworder.mobileno = request.POST.get('mobileno')
    neworder.address = request.POST.get('address')
    neworder.country = request.POST.get('country')
    neworder.city = request.POST.get('city')
    neworder.state = request.POST.get('state')
    neworder.zipcode = request.POST.get('zipcode')

    neworder.payment_mode = request.POST.get('payment_mode')
    neworder.payment_id = request.POST.get('payment_id')
    ct = Cart.objects.get(cart_id=cart_id(request))
    cart = Items.objects.filter(cart =ct)
    cart_total_price = 0
    for item in cart:
        cart_total_price += (item.products.price * item.quantity)

    neworder.total_price = cart_total_price
    trackno = 'shyni' + str(random.randint(1111111, 9999999))
    while Order.objects.filter(tracking_no=trackno) is None:
        trackno = 'shyni' + str(random.randint(1111111, 9999999))
    neworder.tracking_no = trackno
    neworder.save()
    ct = Cart.objects.get(cart_id=cart_id(request))
    neworderitem = Items.objects.filter(cart = ct)
    for item in neworderitem:
        Itemorder.objects.create(
            ord=neworder,
            product=item.products,
            price=item.products.price,
            quantity=item.quantity
        )
        # to decrese the product quantity from available stock
        orderproduct = Product.objects.filter(id=item.products_id).first()
        orderproduct.stock = orderproduct.stock - item.quantity
        orderproduct.save()
    ct = Cart.objects.get(cart_id=cart_id(request))
    Items.objects.filter(cart=ct).delete()
    messages.success(request, 'Your order has been placed successfully')

    payMode = request.POST.get('payment_mode')

    if ( payMode == "Paid by Paypal"):
        return JsonResponse({'status': "Your order has been placed successfully"})

    return redirect('/')






def my_orders(request):
    myorder=Order.objects.filter(user= request.user)

    return render(request,'myorder.html',{'myorder':myorder})

def vieworder(request,t_no):
    order= Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitem=Itemorder.objects.filter(ord=order)

    context={'order':order,'orderitem':orderitem}

    return render(request,'orderview.html',context)