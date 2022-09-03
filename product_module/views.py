from itertools import product
from turtle import title
from urllib import request
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from site_module.models import SiteBanner
from utils.http_service import get_client_ip
from utils.convertors import group_list
from .models import Product, ProductCategory, ProductBrand, ProductComment, ProductVisit, ProductGallery
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query



class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get("product_favorites")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPositions.product_detail)
        context['product_galleries_group'] = group_list(list(ProductGallery.objects.filter(product_id=loaded_product.id).all()), 3)
        context['product_comments'] = ProductComment.objects.filter(product_id = loaded_product.id , is_active=True).order_by('-create_date')
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context



class SearchResultsView(ListView):
    model = Product
    template_name = 'product_module/product_search_list.html'
    context_object_name = 'products'
    def get_queryset(self):
        query = self.request.GET.get('q')
        products=Product.objects.filter(title__contains = query).values()
        print( " size =>  " + str(products.count()) )
        return products




class AddProductFavorite(View):
    def post(self, request):
        product_id = request.get
        product = Product.objects.get(pk=product_id)
        request.session["product_favorites"] = product_id
        return redirect(product.get_absolute_url())


@login_required
def add_product_comment(request: HttpRequest):
    if request.user.is_authenticated:
        product_id = request.POST.get('productid')
        product_title = request.POST.get('title')
        product_description = request.POST.get('description')
        print(product_id )
        new_comment = ProductComment(title = product_title , description = product_description , user_id = request.user.id , product_id = product_id)
        new_comment.save()
        # context = {
        #     'product': Product.objects.filter(id=product_id).values(),
        #     'banners': SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPositions.product_detail),
        #     'product_galleries_group': group_list(list(ProductGallery.objects.filter(product_id=product_id).all()), 3),
        #     'product_comments': ProductComment.objects.filter(product_id = product_id).order_by('-create_date')

        # }


        # return render(request, 'product_module/product_detail.html', context)
        product =  Product.objects.get(id=product_id)
        return redirect('/products/' + product.slug)

    return HttpResponse('response')





def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)



def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)



#remain this part
# def add_product_comment(request: HttpRequest):
#     if request.user.is_authenticated:
#         commnent_title = request.POST.get('title')
#         product_id = request.POST.get('product_id')
#         commnent_description = request.POST.get('description')
#         new_comment = ProductComment(product_id=product_id, text=commnent_title, description= commnent_description , user_id = request.user.id)
#         new_comment.save()
       
#         return render("")

#     return HttpResponse('response')



