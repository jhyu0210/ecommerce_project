# Stripe 
import json
import stripe


from django.conf import settings
from django.http import JsonResponse


from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required

from store.forms import OrderForm
from store.cart import Cart
from .models import Product, Category,Order,OrderItem
from django.db.models import Q

# Create your views here.
# from userprofile.models import User

def product_detail(request,category_slug,slug):
  # for test
  # cart=Cart(request)
  # print(cart.get_total_cost())
  
  print('Slug:: ',slug)
  product = get_object_or_404(Product, slug=slug)
  return render(request, 'store/product_detail.html',{
    'product':product
  })

def category_detail(request,slug):
  category = get_object_or_404(Category,slug=slug)
  products = category.products.filter(status=Product.ACTIVE)
  print("Category Products: ",products)
  return render(request, 'store/category_detail.html',{
    'category': category,
    'products':products
  })
  
def search(request):
  query = request.GET.get('query','')
  products = Product.objects.filter(status=Product.ACTIVE).filter(Q(title__icontains=query) | Q(description__icontains=query))
  return render(request, 'store/search.html',{
    'query': query,
    'products': products
  })
  
def add_to_cart(request, product_id):
  cart = Cart(request)
  cart.add(product_id)

  return redirect('frontpage')

@login_required
def checkout(request):
  cart= Cart(request)
  if cart.get_total_cost() == 0:
    return redirect('cart_view')
  
  if request.method=="POST":
    data=json.loads(request.body)
    
    print('json decoded data:::',data)
    first_name = data['first_name']
    last_name = data['last_name']
    address = data['address']
    zipcode = data['zipcode']
    city = data['city']
    
    if first_name and last_name and address and zipcode and city:
      form = OrderForm(request.POST)
    
    # if form.is_valid():
      
    total_price = 0
    
    # for stripe
    items=[]
    
    for item in cart:
      product= item['product']
      total_price += product.price * int(item['quantity'])
      # for stripe
      items.append({
        'price_data': {
          'currency': 'usd',
          'product_data': {
            'name': product.title,
          },
          'unit_amount':product.price,
        },
        'quantity':item['quantity']
      })
      
    print("Total Price in order:: ",total_price)
    print("Items to payment Stripe:: ",items)
    
    stripe.api_key = settings.STRIPE_SECRET_KEY # say hello to stripe
    session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items = items,
      mode='payment',
      # success_url = settings.WEBSITE_URL+'/cart/success',
      success_url = f'{settings.WEBSITE_URL}cart/success/',
      cancel_url = f'{settings.WEBSITE_URL}cart/',
      # cancel_url = settings.WEBSITE_URL+'/cart/',
    )
    payment_intent = session.payment_intent
    
    # print("Payment_Intent::", payment_intent)

    order = Order.objects.create(
    # order= form.save(commit=False)
      first_name = data['first_name'],
      last_name = data['last_name'],
      address = data['address'],
      zipcode = data['zipcode'],
      city = data['city'],
      
      created_by=request.user,
      
      # 2.for stripe payment add is_order.paid = True
      is_paid = True,
      payment_intent = payment_intent,
      
      paid_amount = total_price,
    )
    # order.save()
    
    for item in cart:
      product = item['product']
      quantity = int(item['quantity'])
      price = product.price * quantity
      
      item = OrderItem.objects.create(order=order, product=product,price=price, quantity=quantity)
      
    cart.clear()
    
    # return redirect('myaccount')
    return JsonResponse({'session':session, 'order':payment_intent})
  else:
    form=OrderForm()
  
  # 1. adding pubkey for stripe
  
  return render(request,'store/checkout.html',{
    'cart':cart,
    'form':form,
    'pub_key': settings.STRIPE_PUB_KEY,
  })

def remove_from_cart(request,product_id):
  cart =Cart(request)
  
  # form = OrderForm()
  cart.remove(product_id)
  
  return redirect('cart_view')

def success(request):
  return render(request, 'store/success.html')

def change_quantity(request, product_id):
  cart =Cart(request)
  
  action = request.GET.get('action','')
  
  if action:
    quantity = 1
    if action == 'decrease':
      quantity = -1
    
    cart.add(product_id, quantity, True)
  return redirect('cart_view')

def cart_view(request):
  cart = Cart(request)
  
  return render(request,'store/cart_view.html',{
    'cart':cart
  })