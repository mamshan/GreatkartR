from django.shortcuts import render

from store.models import Product
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail

def home(request):

 
   
    width = Product.objects.values('width').filter(is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('width') 
    height = Product.objects.values('height').filter(is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('height') 
    diameter = Product.objects.values('diameter').filter(is_available=True).exclude(width__exact='').annotate(Count('id')).order_by('diameter') 

  

    products = Product.objects.all().filter(width__exact='235',is_available=True)
    context = {
        'products': products,
        'width': width,
        'height': height,
        'diameter': diameter,
    }
    return render(request, 'home.html', context)



def brands(request):
  
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
    return render(request, 'home/brands.html', context)

def faq(request):
    return render(request, 'home/faq.html')

def contactus(request):


    subject = "Inquiry"
    message = "Inquiry from " + str(request.GET.get('name')) + " / " + str(request.GET.get('phone'))  +  " about " + str(request.GET.get('inqu')) 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ["shano1106@gmail.com", ]
    send_mail( subject, message, email_from, recipient_list )

    return JsonResponse({"status": 1 }, status=200)