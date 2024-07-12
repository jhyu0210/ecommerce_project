from django.urls import path,include

from . import views
urlpatterns = [
    path('search/',views.search,name='search'),
    path('hx_menu_cart', views.hx_menu_cart, name='hx_menu_cart'),
    path('hx_cart_total', views.hx_cart_total, name='hx_cart_total'),
    path('hx_add-to-cart/<int:product_id>/', views.hx_add_to_cart,name='hx_add_to_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart,name='add_to_cart'),
    path('update-cart/<int:product_id>/<str:action>/', views.update_cart,name='update_cart'),

    path('remove-from-cart/<str:product_id>/', views.remove_from_cart,name='remove_from_cart'),
    # path('change-quantity/<str:product_id>/', views.change_quantity,name='change_quantity'),
    path('cart/', views.cart_view,name='cart_view'),
    path('cart/start_order/', views.start_order, name='start_order'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('cart/success/', views.success,name='success'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:slug>/', views.product_detail, name='product_detail'),
]
