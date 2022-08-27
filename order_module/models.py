
from django.db import models
from product_module.models import Product
from account_module.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True ,verbose_name= 'خریدار')
    address = models.CharField(max_length=250  , verbose_name= 'آدرس 1' )
    address_second = models.CharField(max_length=250,null=True , verbose_name= 'آدرس 2')
    postal_code = models.CharField(max_length=20 , verbose_name= 'کد پستی' ) 
    province = models.CharField(max_length=100, null=True , verbose_name= 'استان' , default= "تهران") 
    city = models.CharField(max_length=100 , verbose_name= 'شهر' , default= "شهریار")
    created = models.DateTimeField(auto_now_add=True , verbose_name= 'زمان ایجاد')
    updated = models.DateTimeField(auto_now=True , verbose_name= 'زمان ویرایش' )
    paid = models.BooleanField(default=False , verbose_name= 'پرداخت شده ؟' )
    total_price = models.DecimalField(max_digits=10, decimal_places=2 , default=0 , verbose_name= 'مجموع قیمت')

    class Meta:
        verbose_name = 'سفارشات'
        verbose_name_plural = 'سفارشات'
        ordering = ('-created',)


    def __str__(self):
        return 'Order {} {}'.format(self.user, self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.order_items.all())



class OrderItem(models.Model):
    order = models.ForeignKey(Order,
    related_name='order_items',
    on_delete=models.CASCADE, verbose_name= 'شناسه سفارش'
    )
    product = models.ForeignKey(Product,
    related_name='order_products',
    on_delete=models.CASCADE, verbose_name= 'محصول'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2  , verbose_name= 'قیمت واحد')
    quantity = models.PositiveIntegerField(default=1 , verbose_name= 'تعداد محصول')

    class Meta:
        verbose_name = 'جزییات سفارش'
        verbose_name_plural = 'جزییات سفارش'
       


    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity