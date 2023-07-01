from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path("user_register", views.user_register, name='user_register'),
    path("store_register", views.store_register, name='store_register'),
    path("store_login", views.store_login, name='store_login'),
    path("user_login", views.user_login, name='user_login'),
    path("add_product", views.add_product, name='add_product'),
    path("update_product", views.update_product, name='update_product'),
    path("delete_product", views.delete_product, name='delete_product'),
    path("store_product_list", views.store_product_list, name='store_product_list'),
    path("user_store_list", views.user_store_list, name='user_store_list'),
    path("product_of_store_list", views.product_of_store_list, name='product_of_store_list'),
    path("add_to_cart", views.add_to_cart, name='add_to_cart'),
    path("update_cart", views.update_cart, name='update_cart'),
    path("remove_signle_item", views.remove_signle_item, name='remove_signle_item'),
    path("remove_all_item", views.remove_all_item, name='remove_all_item'),
    path("cart_detail", views.cart_detail, name='cart_detail'),
]