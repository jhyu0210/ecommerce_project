from django.shortcuts import get_object_or_404, render

from store.models import Product

# Create your views here.
def product(request,slug):
    product = get_object_or_404(Product,slug=slug)
    return render(request, 'product/product.html',{"product":product})