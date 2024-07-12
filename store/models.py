from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
  title = models.CharField(max_length=50)
  slug = models.SlugField(max_length=50)
  class Meta:
    verbose_name_plural = 'Categories'
    ordering = ('title',)

  def __str__(self):
    return self.title
  
  

class Product(models.Model):
  DRAFT = 'draft'
  WAITING_APPROVAL = 'waitingapproval'
  ACTIVE = 'active'
  DELETED = 'deleted'
  
  STATUS_CHOICES = (
    (DRAFT, 'Draft'),
    (WAITING_APPROVAL, 'Waiting Approval'),
    (ACTIVE, 'Active'),
    (DELETED, 'Deleted'),
  )
  
  
  user = models.ForeignKey(User,related_name='products',on_delete=models.CASCADE)
  category = models.ForeignKey(Category,related_name='products', on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  slug = models.SlugField(max_length=50)
  description = models.TextField(blank=True)
  price = models.IntegerField()
  image = models.ImageField(upload_to='upload/product_images/', blank=True,null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=ACTIVE)
  
  def __str__(self):
    return self.title
  
  def get_display_price(self):
    return self.price / 100
  
  class Meta:
    ordering=('-created_at',) # must be a tuple
    
class Order(models.Model):
  first_name= models.CharField(max_length=255)
  last_name= models.CharField(max_length=255)
  address= models.CharField(max_length=255)
  zipcode= models.CharField(max_length=255)
  city= models.CharField(max_length=255)
  paid_amount = models.IntegerField(blank=True, null=True)
  is_paid = models.BooleanField(default=False)
  # merchant_id = models.CharField(max_length=255)
  payment_intent = models.CharField(max_length=255)
  created_by= models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL,null=True)
  created_at= models.DateTimeField(auto_now_add=True)
  class Meta:
    ordering = ('-created_at',)
  
  def get_total_price(self):
    if self.paid_amount:
      return self.paid_amount / 100
    return 0

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
  product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
  price = models.IntegerField()
  quantity = models.IntegerField(default=1)
  
  def get_total_price(self):
    return self.price / 100