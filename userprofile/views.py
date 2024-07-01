
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from .models import Userprofile
from store.models import Product, Category, OrderItem, Order
from store.forms import ProductForm
# Create your views here.
def vendor_detail(request,pk):
  user = User.objects.get(pk=pk)
  products = user.products.filter(status=Product.ACTIVE)
  
  return render(request, 'userprofile/vendor_detail.html',{
    'user':user,
    'products':products
  })
  
@login_required
def add_product(request):
  if request.method == 'POST':
    form= ProductForm(request.POST,request.FILES)
    
    if form.is_valid():
      title = request.POST.get('title')
      slug = slugify(title)
      product = form.save(commit=False)
      # save to database
      product.user= request.user
      product.slug = slug
      product.save()
      messages.success(request, 'The product was saved!')
      return redirect('my_store')
  else:
    form= ProductForm()
  return render(request, 'userprofile/product_form.html',{'form': form,'title': 'Add Product'})

@login_required
def edit_product(request,pk):
  product= Product.objects.filter(user=request.user).get(pk=pk)
  print("Product to edit:: ",product)
  if request.method == 'POST':
    form= ProductForm(request.POST,request.FILES, instance=product)
    
    if form.is_valid():
      # print("request.POST::: ",request.POST)
      form.save()
      messages.success(request, 'The Changes were saved!')
      return redirect('my_store')
  else:
    form= ProductForm(instance=product)
    
  return render(request, 'userprofile/product_form.html',{
    'title':'Edit Product',
    'form': form,
    'product':product
    })

@login_required
def delete_product(request, pk):
  product = Product.objects.filter(user=request.user).get(pk=pk)
  print("Product to delete:: ",product)
  product.status = Product.DELETED
  product.save()
  messages.success(request, 'The product was deleted!')
  return redirect('my_store')
  
@login_required
def my_store(request):
  products = request.user.products.exclude(status=Product.DELETED) #??
  order_items = OrderItem.objects.filter(product__user=request.user)
  # products = Product.objects.filter(user=request.user) #??
  # print("my store products:: ",request.user.products.all())
  # print("My store:: ",products)
  return render(request,'userprofile/my_store.html',{
    'products': products,
    'order_items': order_items
  })
  
@login_required
def my_store_order_detail(request, pk):
  order = get_object_or_404(Order, pk=pk)
  return render(request, 'userprofile/my_store_order_detail.html',{
    'order': order
  })

@login_required
def myaccount(request):
  return render(request, 'userprofile/myaccount.html')

def user_logout(request):
  logout(request)
  # return render(request,'userprofile/logout.html')
  return redirect('frontpage')
  
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            userprofile = Userprofile.objects.create(user=user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()
    
    return render(request, 'userprofile/signup.html', {
        'form': form
    })

