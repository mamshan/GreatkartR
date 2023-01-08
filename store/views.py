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

def store(request, category_slug=None, brand=None):
    
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True).order_by('-price') 
        brands = Product.objects.values('brand').filter(category=categories, is_available=True).annotate(Count('id'))
        width = Product.objects.values('width').filter(category=categories, is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('width') 
    
        if brand is not None:
            products = Product.objects.all().filter(category=categories,brand=brand, is_available=True).order_by('-price') 
            brands = Product.objects.values('brand').filter(category=categories, brand=brand,is_available=True).annotate(Count('id'))
            width = Product.objects.values('width').filter(category=categories,brand=brand, is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('width') 
    
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-price')  
        brands = Product.objects.values('brand').filter(is_available=True).annotate(Count('id'))
        width = Product.objects.values('width').filter(is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('width') 
    
        if brand is not None:
            products = Product.objects.all().filter(brand=brand, is_available=True).order_by('-price') 
            brands = Product.objects.values('brand').filter(brand=brand,is_available=True).annotate(Count('id'))

    product_count = products.count()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(products, 12)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'width':width,
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
    paginator = Paginator(products, 10)
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context=context)



def product_detail(request, category_slug,  product_slug, brand):
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

    try:
        relastedprod = Product.objects.filter(width__icontains=single_product.width, height__icontains=single_product.height, diameter__icontains=single_product.diameter,is_available=True).exclude(id=single_product.id)
    except OrderProduct.DoesNotExist:
        relastedprod = None


    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)



    context = {
        'single_product': single_product,
        'in_cart': in_cart if 'in_cart' in locals() else False,
        'product_gallery':product_gallery,
        'orderproduct':orderproduct,
        'relastedprod': relastedprod
    }
    return render(request, 'store/product_detail.html', context=context)




def search(request):
    if 'width' in request.GET:
        width = request.GET.get('width')
        profile = request.GET.get('profile')
        diameter = request.GET.get('diameter')

        products = Product.objects.order_by('-created_date').filter(width__icontains=width, height__icontains=profile, diameter__icontains=diameter,is_available=True)
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
        width = request.GET.get('width') 
        profile = request.GET.get('profile')  
        width = Product.objects.values('diameter').filter(width__icontains=width,height__icontains=profile,is_available=True).exclude(width__exact='').annotate(Count('id'))
        product_count = width.count()    
    if 'rim' in request.GET:
        width = request.GET.get('width') 
        profile = request.GET.get('profile') 
        rim = request.GET.get('rim')  
        width = Product.objects.values('terrain').filter(width__icontains=width,height__icontains=profile,diameter__icontains=rim,is_available=True).exclude(terrain__exact='').annotate(Count('id'))
        product_count = width.count()        

    return JsonResponse({"width": list(width), "product_count": product_count }, status=200)


def search(request):
    if 'width' in request.GET:
        width = request.GET.get('width')
        profile = request.GET.get('profile')
        diameter = request.GET.get('diameter')
        terrain = request.GET.get('terrain')


        view = request.GET.get('view1')

        if request.GET.get('terrain') =="Any":
            products = Product.objects.order_by('-created_date').filter(width__icontains=width, height__icontains=profile, diameter__icontains=diameter,is_available=True)
            product_count = products.count()
        else:
            products = Product.objects.order_by('-created_date').filter(width__icontains=width, height__icontains=profile, diameter__icontains=diameter, terrain__icontains=terrain,is_available=True)
            product_count = products.count()

    widths = Product.objects.values('width').filter(is_available=True).exclude(width__exact='').annotate(Count('id'))
   
 

    context = {
        'products': products,
        'q': width,
        'product_count': product_count,
        'width': widths,
        'swidth': width,
        'sprofile': profile,
        'sdiameter': diameter,
        'sterrain': terrain,
        
    }



    if view == "view1":   
        return render(request, 'store/store_search.html', context=context)
    else:
        return render(request, 'store/store_search_view.html', context=context)