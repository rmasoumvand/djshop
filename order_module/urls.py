from django.urls import path
from . import views

urlpatterns = [
    
    path('create', views.order_create, name='order_create'),
    path('process', views.order_save, name='order_save'),

    # url('create', views.order_create, name='order_create'),
    # url('process', views.order_save, name='order_save'),
]
