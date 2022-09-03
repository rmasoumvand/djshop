"""eshop_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from azbankgateways.urls import az_bank_gateways_urls
from apppayment.views import go_to_gateway_view,callback_gateway_view
from product_module.views import SearchResultsView


urlpatterns = [
    path('', include('home_module.urls')),
    path('', include('account_module.urls')),
    path('articles/', include('article_module.urls')),
    path('contact-us/', include('contact_module.urls')),
    path('products/', include('product_module.urls')),
    path('user/', include('user_panel_module.urls')),
    path('orders/', include('order_module.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('go-to-gateway/<orderid>', go_to_gateway_view),
    path('callback-gateway/', callback_gateway_view),
    path('cart/', include('cart_module.urls') ),#include('cart_module.urls')
    path('admin/', admin.site.urls),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
