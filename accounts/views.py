from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from products.models import Product

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        if(request.POST["password1"] != request.POST["password2"]):
            return render(request, 'accounts/signup.html', {'error': 'As passwords não são iguais'})
        try:
            user = User.objects.create_user(((request.POST['email']).split("@"))[0], request.POST['email'], request.POST["password1"])
        except Exception as e:
            return render(request, 'accounts/signup.html', {'error': 'Já existe uma conta com esse email'})
        user.save()
        user.cart = Cart(id=0, total_price=0, user=user)
        user.userprofile.name = request.POST['first_name']
        user.userprofile.last_name = request.POST['last_name']
        user.userprofile.country = request.POST['country']
        user.userprofile.address = request.POST['address']
        user.userprofile.city = request.POST['city']
        user.userprofile.zip_code = request.POST['zip_code']
        user.userprofile.localidade = request.POST['localidade']
        user.userprofile.cell_number = request.POST['cell_number']
        user.userprofile.email = request.POST['email']
        user.save()
        user.userprofile.save()
        login(request, user)
        return redirect('index_accounts')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return render(request, 'accounts/login.html', {'error': 'Não há utilizador com esse email ou a palavra passe está errada'})
        authenticated = authenticate(username=user.username, password=password)
        if authenticated is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('index_accounts')
        else:
            return redirect('index_accounts')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index_accounts')

@login_required
def add_to_favourites(request):
    if request.method == 'POST':
        id = request.POST['id']
        user = request.user.userprofile
        user.favourite_products.add(Product.objects.get(id=id))
    return redirect(saved_products)

@login_required
def user_info(request):
    if request.method == 'POST':
        if request.POST['first_name']:
            request.user.userprofile.name = request.POST['first_name']
        if request.POST['last_name']:
            request.user.userprofile.last_name = request.POST['last_name']
        if request.POST['country']:
            request.user.userprofile.country = request.POST['country']
        if request.POST['address']:
            request.user.userprofile.address = request.POST['address']
        if request.POST['city']:
            request.user.userprofile.city = request.POST['city']
        if request.POST['zip_code']:
            request.user.userprofile.zip_code = request.POST['zip_code']
        if request.POST['localidade']:
            request.user.userprofile.localidade = request.POST['localidade']
        if request.POST['cell_number']:
            request.user.userprofile.cell_number = request.POST['cell_number']
        if request.POST['email']:
            request.user.userprofile.email = request.POST['email']
        request.user.userprofile.save()
        return render(request, 'accounts/sucessfulChange.html')
    else:
        user = request.user
        context = {'user' : user}
        return render(request, 'accounts/user_info.html', context)

@login_required
def saved_products(request):
    user = request.user
    context = {'favourite_products': user.userprofile.favourite_products}
    return render(request, 'accounts/saved_products.html', context)

@login_required(login_url="/accounts/login/")
def restricted_view(request):
    return render(request, 'accounts/restrictedAcess.html')

def index_accounts(request):
    return render(request, 'accounts/index_accounts.html')


def delete_all_users(request):
    if( "HTTP_INEEDTODELETEUSERS" in dict(request.META.items())):
        for user in User.objects.all():
            if(user.userprofile.anonymous_user == True):
                logout(user)
                user.delete()
        return HttpResponse("Users deleted")
    else:
        return HttpResponse("No Header")
