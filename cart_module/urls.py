from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<product_id>/', views.cart_add, name='cart_add'),
    path('add_q/<product_id>/', views.cart_add_q, name='cart_add_q'),
    path('remove/<product_id>/', views.cart_remove, name='cart_remove'),

]
