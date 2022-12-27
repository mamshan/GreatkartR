from django.shortcuts import render

from store.models import Product
from django.db.models import Sum, Count

def home(request):

 
   
    width = Product.objects.values('width').filter(is_available=True).exclude(width__exact='').annotate(Count('id'))
    height = Product.objects.values('height').filter(is_available=True).exclude(width__exact='').annotate(Count('id'))
    diameter = Product.objects.values('diameter').filter(is_available=True).exclude(width__exact='').annotate(Count('id'))

 

    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
        'width': width,
        'height': height,
        'diameter': diameter,
    }
    return render(request, 'home.html', context)