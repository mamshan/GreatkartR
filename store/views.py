from category.models import Category , SubCategory
from orders.models import OrderProduct
from store.models import Product, ProductGallery
from django.shortcuts import get_object_or_404, redirect, render
from carts.views import _cart_id
from carts.models import Cart, CartItem
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.db.models import Q
from django.db.models import Sum
from django.db.models import Sum, Count
from django.http import JsonResponse

def store(request, category_slug=None):
    
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True).order_by('id')
        brands = Product.objects.values('brand').filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') 
        brands = Product.objects.values('brand').filter(is_available=True)

    
    product_count = products.count()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 3)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'brands': brands
    }
    return render(request, 'store/store.html', context=context)



def store1(request,  category_slug=None, subcategory_slug=None):
    
    if subcategory_slug is not None:
        categories = get_object_or_404(SubCategory, slug=subcategory_slug)
        products = Product.objects.all().filter(subcategory=categories, is_available=True).order_by('id')
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')

    product_count = products.count()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 3)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context=context)



def product_detail(request, category_slug,  product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None  

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)



    context = {
        'single_product': single_product,
        'in_cart': in_cart if 'in_cart' in locals() else False,
        'product_gallery':product_gallery,
        'orderproduct':orderproduct
    }
    return render(request, 'store/product_detail.html', context=context)




def search(request):
    if 'width' in request.GET:
        width = request.GET.get('width')
        profile = request.GET.get('profile')
        diameter = request.GET.get('diameter')

        products = Product.objects.order_by('-created_date').filter(width__icontains=width, height__icontains=profile, diameter__icontains=diameter)
        product_count = products.count()

    context = {
        'products': products,
        'q': width,
        'product_count': product_count
    }
    return render(request, 'store/store.html', context=context)

def get_sizes(request):
    width =""
    if 'width' in request.GET:
        width = request.GET.get('width') 
        width = Product.objects.values('height').filter(width__icontains=width,is_available=True).exclude(width__exact='').annotate(Count('id'))
        product_count = width.count()

    if 'profile' in request.GET:
        width = request.GET.get('profile') 
        width = Product.objects.values('diameter').filter(height__icontains=width,is_available=True).exclude(width__exact='').annotate(Count('id'))
        product_count = width.count()    
        

    return JsonResponse({"width": list(width), "product_count": product_count }, status=200)