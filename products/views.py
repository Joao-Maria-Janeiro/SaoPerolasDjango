from django.shortcuts import render, redirect
from .models import Product, BackGroundImage
from .forms import CreateProduct
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    image = BackGroundImage.objects.order_by('id')
    try:
        imagez = image[0]
        colar = image[1]
        pulseira = image[2]
        brinco = image[3]
    except Exception as e:
        print(e)
    context = {'image': imagez, 'colar': colar, 'pulseira': pulseira, 'brinco': brinco}
    return render(request, 'products/index.html', context)

def products(request):
    colar = Product.objects.order_by('-id')

    context = {'colar': colar}
    return render(request, 'products/compridos.html', context)

def colares(request, id):
    colar = Product.objects.get(id=id)
    context = {'colar': colar}
    return render(request, 'products/product_page.html', context)

def pulseiras(request):
    pulseira = Product.objects.order_by('-id')

    context = {'pulseira': pulseira}
    return render(request, 'products/pulseiras.html', context)

def pulseira_individual(request, id):
    pulseira = Product.objects.get(id=id)
    context = {'pulseira': pulseira}
    return render(request, 'products/pulseira.html', context)

def contactos(request):
    return render(request, 'products/contactos.html')

def brincos(request):
    brinco = Product.objects.order_by('-id')

    context = {'brinco': brinco}
    return render(request, 'products/brincos.html', context)

def brinco_individual(request, id):
    brinco = Product.objects.get(id=id)
    context = {'brinco': brinco}
    return render(request, 'products/brinco.html', context)


@login_required(login_url="/accounts/login/")
def product_create(request):
    if request.method == 'POST':
        form = CreateProduct(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                if(request.POST['colar'] == "on"):
                    colar = True
            except MultiValueDictKeyError:
                colar = False
            try:
                if(request.POST['pulseira'] == "on"):
                    pulseira = True
            except MultiValueDictKeyError:
                pulseira = False
            try:
                if(request.POST['brinco'] == "on"):
                    brinco = True
            except MultiValueDictKeyError:
                brinco = False


            price=request.POST['price']
            a=price.split()
            a.reverse()
            price = int(" ".join(a))

            print("I GOT HERE")
            new_product = Product(name=request.POST['name'], description=request.POST['description'], price=price, image=request.FILES['image'], colar=colar, brinco=brinco, pulseira=pulseira)
            print("I GOT FURTHER")
            try:
                new_product.save()
            except Exception as e:
                print(e)

            return redirect('products')
        else:
            print (form.errors)
            return HttpResponse('Error occurred, product was not added' + str(form.errors))
    else:
        form = CreateProduct()
        return render(request, 'products/create_product.html', {'form': form})
