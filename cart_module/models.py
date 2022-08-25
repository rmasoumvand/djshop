from django.db import models

from account_module.models import User
from product_module.models  import Product

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True , verbose_name= "خریدار")
    created = models.DateTimeField(auto_now_add=True, verbose_name= "زمان ایجاد ")
    updated = models.DateTimeField(auto_now=True , verbose_name= "زمان ویرایش ")
    paid = models.BooleanField(default=False , verbose_name= "   پردخت شده ؟ ")
    is_in_order = models.BooleanField(default=False , verbose_name= " موجود در سفارش ؟")

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد خرید'
        ordering = ('-created',)

    def __str__(self):
        return 'cart {}'.format(self.user.email)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',
    null=True,
    on_delete=models.CASCADE,verbose_name= 'شناسه سبد خرید'
    )
    product = models.ForeignKey(Product,
    related_name='cart_items',
    on_delete=models.CASCADE,verbose_name= 'شناسه محصول'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0 , verbose_name= 'قیمت واحد ')
    quantity = models.PositiveIntegerField(default=1 , verbose_name= 'تعداد محصول')

    class Meta:
        verbose_name = 'جزییات سبد خرید'  
        verbose_name_plural = 'جزییات سبد خرید'
        

    def __str__(self):
        return '{}'.format(self.product.title)

    def get_cost(self):
        return self.price * self.quantity