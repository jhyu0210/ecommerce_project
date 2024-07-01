from django.shortcuts import render

from store.models import Product

# Create your views here.
def frontpage(request):
  products = Product.objects.exclude(status=Product.DELETED)[0:6]
  return render(request, 'core/frontpage.html',{
    'products':products
  })

def aboutpage(request):
  return render(request, 'core/aboutpage.html')