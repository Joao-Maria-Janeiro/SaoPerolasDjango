from django.shortcuts import render, redirect
from .models import Cart, Cart_userless, CartProduct, ShippingDetails, Order, OrderUserless
from .forms import CreateShipphingDetails
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.http import HttpResponse
import datetime
import stripe
from django.conf import settings
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import login
import smtplib
import cart.config_email as config

stripe.api_key = settings.STRIPE_SECRET_KEY


def send_mail(products, shipping_details, receiver_email, total_price):
    print(receiver_email)
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL, config.PASSWORD)
        msg = "Produtos: \n"
        for productz in products:
            msg += "Nome: " + productz.product.name + " | Quantidade: " + str(productz.quantity) + "\n"
        msg += "Preço total: " + str(total_price) + "\n"
        msg += "Detalhes de shipping: \n"
        msg += "Nome Completo: " + shipping_details.full_name + "\nMorada: " +  shipping_details.adress + "\nCidade: " + shipping_details.city + "\nLocalidade: " + shipping_details.localidade + "\nZip: " + shipping_details.zip + "\nPaís: "+ shipping_details.country + "\nNúmero de Telemóvel: " + shipping_details.phone_number
        message = "Subject: {}\n\n{}".format("Nova Compra", msg).encode('utf-8').strip()
        server.sendmail(config.EMAIL, config.RECIEVER_EMAIL, message)
        server.quit()
        print("Sucess: Email Sent!")
    except Exception as e:
        print("E-mail not sent!")
        print(e)


def stripeInfos(request, shipping_details, cart):
    token = request.POST['stripeToken']

    charge = stripe.Charge.create(
        amount=100*cart.total_price,
        currency='eur',
        description='Products',
        source=token,
        receipt_email=shipping_details.email,
    )

def clear_cart(cart):
    cart.products.clear()
    cart.total_price = 0
    cart.save()

def checkNew(cart, id):
    found = 0
    for productz in cart.products.all():
        if productz.product.name == Product.objects.get(id=id).name:
            product = productz
            found = 1
            cart.products.remove(product)
            product.quantity += 1
            product.save()
            cart.products.add(product)
    return found

def calc_price(cart):
    if(len(cart.products.all()) == 0):
        cart.total_price = 0
        return
    for productz in cart.products.all():
        price = int(productz.product.price) * (productz.quantity)
        cart.total_price += price
    cart.total_price +=  3

# Create your views here.
def add_to_cart(request, id):
    if request.user.is_authenticated:
        found = 0
        user = request.user
        cart = user.cart
        found = checkNew(cart, id)
        if found == 0:
            product = CartProduct(product=Product.objects.get(id=id))
            product.save()
            cart.products.add(product)
        cart.total_price = 0
        calc_price(cart)
        cart.save()
    else:
        name = str(uuid.uuid4())
        email = name + "@gmail.com"
        user = User.objects.create_user(name, email, 'johnpassword')
        user.save()
        user.userprofile.anonymous_user = True
        user.userprofile.save()
        # user.save()
        login(request, user)
        found = 0
        cart = user.cart
        found = checkNew(cart, id)
        if found == 0:
            product = CartProduct(product=Product.objects.get(id=id))
            product.save()
            cart.products.add(product)
        cart.total_price = 0
        calc_price(cart)
        cart.save()
    return redirect('display_cart')

def remove_from_cart(request, id):
    if request.user.is_authenticated:
        user = request.user
        cart = user.cart
        product = CartProduct.objects.get(id=id)
        cart.products.remove(product)
        cart.total_price = 0
        calc_price(cart)
        cart.save()
    else:
        return HttpResponse('Cart is empty')
    return redirect('display_cart')

@login_required
def shipping_details(request):
    if request.method == 'POST':
        if request.POST['full_name'] == '':
            request.user.userprofile.use_saved_details = True
            request.user.userprofile.save()
            return redirect('order_details')
        else:
            form = CreateShipphingDetails(request.POST)
            if form.is_valid():
                form.email = request.POST['email']
                details = form.save()
                request.user.userprofile.use_saved_details = False
                request.user.userprofile.shipping_details_id = details.id
                request.user.userprofile.save()
                return redirect('order_details')
    else:
        form = CreateShipphingDetails()
        return render(request, 'cart/shippingDetails.html', {'form': form})

@login_required
def order_details(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.cart.total_price != 0 :
                cart = request.user.cart
                total_price = cart.total_price
                if request.user.userprofile.use_saved_details == True:
                    shipping_details = ShippingDetails(full_name = request.user.username + ' ' + request.user.userprofile.last_name, adress = request.user.userprofile.address, city = request.user.userprofile.city, localidade = request.user.userprofile.localidade, zip = request.user.userprofile.zip_code, country = request.user.userprofile.country, phone_number = request.user.userprofile.cell_number, email = request.user.userprofile.email)
                    shipping_details.save()
                else:
                    shipping_details = ShippingDetails.objects.get(id=request.user.userprofile.shipping_details_id)
                date_ordered = datetime.datetime.now()
                order = Order(cart=cart, total_price=total_price, shipping_details=shipping_details, date_ordered=date_ordered)
                order.save()
                publishKey = settings.STRIPE_PUBLISHABLE_KEY
                if request.method == 'POST':
                        try:
                            stripeInfos(request, shipping_details, cart)
                            send_mail(cart.products.all(), shipping_details, shipping_details.email, cart.total_price)
                            clear_cart(cart)
                            return render(request, 'cart/SuccessFulOrder.html')

                        except stripe.error.CardError as e:
                            return render(request, 'cart/cardError.html')

                context = {
                    'order': order,
                    'STRIPE_PUBLISHABLE_KEY': publishKey
                }
            else:
                return HttpResponse('Empty cart or shipping information missing')
        else:
            return HttpResponse('Empty cart or shipping information missing')
        return render(request, 'cart/OrderDetails.html', {'order':order, 'context':context})
    else:
        if request.user.is_authenticated:
            if request.user.cart.total_price != 0:
                cart = request.user.cart
                return render(request, 'cart/OrderDetails.html', {'cart': cart})
        else:
            return HttpResponse('Empty cart or shipping information missing')


@login_required
def increase_quantity(request, id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
    if request.user.is_authenticated:
        user = request.user
        cart = user.cart
    else:
        return HttpResponse('Cart is empty')
    product = CartProduct.objects.get(id=id)
    if product.quantity + quantity >= 0:
        if(product.quantity + quantity == 0):
            cart.products.remove(product);
        else:
            product.quantity += quantity
            product.save()
    cart.total_price = 0
    calc_price(cart)
    cart.save()
    return redirect('display_cart')

def display_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = user.cart
    else:
        return HttpResponse('Cart is empty')
    return render(request, 'cart/display_cart.html', {'cart': cart})
