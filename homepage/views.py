

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404


from .models import Product, Category


def home(request,c_slug=None):
    c_page = None
    product = None
    if c_slug != None:
        ctg_page = get_object_or_404(Category, slug=c_slug)
        product = Product.objects.filter(category=ctg_page, available=True)
    else:

        product = Product.objects.all().filter(available=True)

    catg = Category.objects.all()
    paginator = Paginator(product, 8)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        pro = paginator.page(page)
    except (EmptyPage, InvalidPage):
        pro = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'product': product, 'catg': catg,'page': pro})

@login_required(login_url = '/login')
def productDetails(request, c_slug, product_slug):

     try:
        product = Product.objects.get(category__slug=c_slug, slug=product_slug)
     except Exception as e:
        raise e

     return render(request, 'product-detail.html', {'pr': product})


def searching(request):
    prod = None
    quary = None
    if 'q' in request.GET:
        quary = request.GET.get('q')
        prod = Product.objects.all().filter(Q(name__contains=quary) | Q(desc__contains=quary))

    return render(request, 'search.html', {'qr': quary, 'pr': prod})
