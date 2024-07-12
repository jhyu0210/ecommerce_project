from django.shortcuts import render
from django.db.models import Q

from store.models import Category, Product

# Create your views here.
def frontpage(request):
  products = Product.objects.exclude(status=Product.DELETED)[0:6]
  return render(request, 'core/frontpage.html',{
    'products':products
  })

def aboutpage(request):
  return render(request, 'core/aboutpage.html')

def shop(request):
  categories = Category.objects.all()
  products = Product.objects.exclude(status=Product.DELETED)
  # products = Product.objects.all()[0:6]
  active_category = request.GET.get('category','')
  # print("Active", active_category)
  if active_category:
    products = products.filter(category__slug=active_category)

  query = request.GET.get('query','')
  if(query):
    products = products.filter(Q(title__icontains=query)| Q(description__icontains=query))

  context={
    "categories": categories,
    "products": products,
    "active_category" : active_category
    }

  return render(request, 'core/shop.html',context)

def product(request,slug):
  product= Product.objects.get(slug=slug)
  return render(request, 'product/product.html',{'product':product})