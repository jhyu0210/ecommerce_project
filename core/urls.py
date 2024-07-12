from django.contrib import admin
from django.urls import path
from core.views import aboutpage, frontpage

from core.views import shop
from core.views import product


urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('about/', aboutpage, name='aboutpage'),
    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>/', product, name='product'),
]