from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path(
        'add/',
        views.add_product,
        name='add_product'
    ),
    path(
        'edit/<slug:slug>/',
        views.edit_product,
        name='edit_product'
    ),
    path(
        'delete/<slug:slug>/',
        views.delete_product,
        name='delete_product'
    ),
    path(
        '<slug:slug>/',
        views.product_detail,
        name='product_detail'
    ),
]
