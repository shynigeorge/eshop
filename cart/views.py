from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from cart.models import Items, Cart
from homepage.models import Product


def cartDetails(request,tot=0,count=0):
    cart_items = None

    try:
        ct = Cart.objects.get(cart_id=cart_id(request))
        cart_items = Items.objects.filter(cart=ct,active=True)
        for i in cart_items:
            tot+=(i.products.price*i.quantity)
            count +=i.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',{'cart':cart_items,'tot':tot,'count':count})

def cart_id(request):
    ct_id=request.session.session_key
    if not ct_id:
        ct_id=request.session.create()
    return ct_id

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=cart_id(request))
        cart.save()
    try:
        c_items=Items.objects.get(products=product,cart=cart)
        if c_items.quantity < c_items.products.stock:
            c_items.quantity+=1
            c_items.save()
    except Items.DoesNotExist:
        c_items=Items.objects.create(products=product,quantity=1,cart=cart)
        c_items.save()
    return redirect('cartdetails')

def min_cart(request,product_id):
    ct=Cart.objects.get(cart_id=cart_id(request))
    prod=get_object_or_404(Product,id=product_id)
    c_items=Items.objects.get(products=prod,cart=ct)
    if c_items.quantity > 1:
        c_items.quantity-= 1
        c_items.save()
    else:
        c_items.delete()
    return redirect("cartdetails")


def delete_cart(request,product_id):
    ct = Cart.objects.get(cart_id=cart_id(request))
    prod = get_object_or_404(Product, id=product_id)
    c_items = Items.objects.get(products=prod, cart=ct)
    c_items.delete()
    return redirect("cartdetails")


