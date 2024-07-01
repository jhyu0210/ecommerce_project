from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings

urlpatterns = [
    path('signup/',views.signup,name='singup'),
    path('login/',auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('myaccount/', views.myaccount, name='myaccount'),
    
    path('my-store/', views.my_store, name='my_store'),
    path('my-store/order-detail/<int:pk>/', views.my_store_order_detail, name='my_store_order_detail'),
    path('my-store/add-product/', views.add_product, name='add_product'),
    path('my-store/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('my-store/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('do-logout/', views.user_logout, name='do-logout'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]
