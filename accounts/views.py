import urllib
from urllib.parse import urlparse
from django.shortcuts import get_object_or_404, render, redirect

from accounts.forms import RegistrationForm ,UserProfileForm, UserForm
from accounts.models import Account , UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
#from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from carts.models import Cart, CartItem
from django.conf import settings
from django.core.mail import send_mail
from carts.views import _cart_id
import requests
from orders.models import Order, OrderProduct 
from django.core.files.base import ContentFile
from django.core.files import File
import urllib3 
from django.core.files.temp import NamedTemporaryFile
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()




            current_site = get_current_site(request=request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            #send_email = EmailMessage(mail_subject, message, to=[email])
            #send_email.send()

            subject = mail_subject
            message = message
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )

            messages.success(
                request=request,
                message="Please confirm your email address to complete the registration"
            )
            return redirect('login') 
        else:
            messages.error(request=request, message="Register failed!")

    else:        
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context=context)

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
        except Exception:
                pass    

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                if cart_items.exists():
                    cart_items = CartItem.objects.filter(cart=cart)
                    for item in cart_items:
                        item.user = user
                        item.save()
            except Exception:
                pass
            auth.login(request,user)
            messages.success(request=request, message="Login successful!")

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    next_page = params["next"]
                    return redirect(next_page)
            except Exception:
                return redirect('dashboard')

            return redirect('dashboard')
        else:
            messages.error(request=request, message="Login failed!")
            return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="You are logged out!")
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request, message="Your account is activated, please login!")
        return render(request, 'accounts/login.html')
    else:
        messages.error(request=request, message="Activation link is invalid!")
        return redirect('home')

@login_required(login_url="login")
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()


    userprofile = UserProfile.objects.filter(user=request.user)

    #userprofile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'orders': orders, 
        'orders_count': orders_count,
        'userprofile':userprofile
    }
    return render(request, "accounts/dashboard.html", context)


def forgotPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request=request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            #send_email = EmailMessage(mail_subject, message, to=[email])
            #send_email.send()

            subject = mail_subject
            message = message
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )

            messages.success(
                request=request, message="Password reset email has been sent to your email address")
    except Exception:
        messages.error(request=request, message="Account does not exist!")
    finally:
        context = {
            'email': email if 'email' in locals() else '',
        }
        return render(request, "accounts/forgotPassword.html", context=context)


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request=request, message='Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request=request, message="This link has been expired!")
        return redirect('home')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, message="Password reset successful!")
            return redirect('login')
        else:
            messages.error(request, message="Password do not match!")
    return render(request, 'accounts/reset_password.html')

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    context = {
        'orders': orders
    }
    return render(request, 'accounts/my_orders.html',context=context)


@login_required(login_url="login")
def edit_profile(request):
    #userprofile = get_object_or_404(UserProfile, user=request.user)
    unew = False
    try:
        unew = UserProfile.objects.filter(user=request.user).exists()
        userprofile = UserProfile.objects.get(user=request.user)
    except Exception:
        if request.method == 'POST':
            userprofile =UserProfileForm(request.POST, instance=request.user)  
        else:
            unew = False
            userprofile =UserProfileForm() 


    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        #profile_form = UserProfileForm( 
        #    request.POST, request.FILES, user_id=request.user 
        #    )
        
        if unew == False:
           
            profile_form =UserProfile(
                user=request.user,
                address_line_1= request.POST['address_line_1'],
                address_line_2= request.POST['address_line_2'],
                city= request.POST['city'],
                state= request.POST['state'],
                country= request.POST['country'], 
            )



        else:
            profile_form = UserProfileForm(request.POST,  instance=userprofile)

       
        #profile_form.profile_picture = request.FILES.profile_picture

        #profile_form = UserProfileForm( 
           #request.POST, request.FILES
        #)
        #profile_form.user_id = request.user

        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)

        if unew == True:
            profile_form = UserProfileForm(instance=userprofile)
        else:
            profile_form = UserProfileForm()        

    context = {
        'user_form': user_form,
        'profile_form': profile_form, 
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html',context=context)

@login_required(login_url="login")
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user= Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request, 'Password Updated Successfully')
                return redirect('change_password')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request,  'Passwrod does not match')
            return redirect('change_password')
    context = {
    }
    return render(request, 'accounts/change_password.html',context=context)


@login_required(login_url="login")
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price*i.quantity

    context = {
        'order': order,
        'order_detail': order_detail,
        'subtotal':subtotal
    }
    return render(request, 'accounts/order_detail.html',context=context)


def orders(request):
        orders = OrderProduct.objects.filter(ordered=True).select_related('order').filter(order__status='New')

        context = {
            'orders': orders,
        }
        return render(request, 'admin/orders.html', context)
    