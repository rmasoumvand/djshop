# Generated by Django 4.0 on 2022-09-04 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_module', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='نام محصول')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/products', verbose_name='تصویر محصول')),
                ('price', models.IntegerField(verbose_name='قیمت به تومان ')),
                ('short_description', models.CharField(db_index=True, max_length=360, null=True, verbose_name='توضیحات کوتاه')),
                ('description', models.TextField(db_index=True, verbose_name='توضیحات اصلی')),
                ('slug', models.SlugField(blank=True, default='', max_length=200, unique=True, verbose_name='عنوان در url')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('is_delete', models.BooleanField(verbose_name='حذف شده / نشده')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='نام برند')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='نام در url')),
                ('is_active', models.BooleanField(verbose_name='فعال / غیرفعال')),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برند ها',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان')),
                ('url_title', models.CharField(db_index=True, max_length=300, verbose_name='عنوان در url')),
                ('is_active', models.BooleanField(verbose_name='فعال / غیرفعال')),
                ('is_delete', models.BooleanField(verbose_name='حذف شده / نشده')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='ProductVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=30, verbose_name='آی پی کاربر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='محصول')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_module.user', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'بازدید محصول',
                'verbose_name_plural': 'بازدیدهای محصول',
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(db_index=True, max_length=300, verbose_name='عنوان')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_tags', to='product_module.product')),
            ],
            options={
                'verbose_name': 'تگ محصول',
                'verbose_name_plural': 'تگ های محصولات',
            },
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'تصویر گالری',
                'verbose_name_plural': 'گالری تصاویر',
            },
        ),
        migrations.CreateModel(
            name='ProductComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان')),
                ('description', models.CharField(max_length=300, verbose_name='توضیحات')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('is_delete', models.BooleanField(default=False, verbose_name='حذف شده / نشده')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='محصول')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account_module.user', verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نظرات محصولات',
                'verbose_name_plural': 'نظرات محصولات',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.productbrand', verbose_name='برند'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='product_categories', to='product_module.ProductCategory', verbose_name='دسته بندی ها'),
        ),
    ]