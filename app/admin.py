from django.contrib import admin
from .models import Category , Product,Order
from django.utils.html import format_html
from django.templatetags.static import static
from import_export.admin import ImportExportModelAdmin
from adminsortable2.admin import SortableAdminMixin
# Register your models here.



class ProductInline(admin.StackedInline):
    model = Product
    extra = 2

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'phone',
        'product',
        'quantity',
        'get_total_price',
        'created_at'
    ]
    list_filter = ['created_at', 'product__category']
    search_fields = ['name', 'phone', 'product__name']
    autocomplete_fields = ['product']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    def get_total_price(self, obj):
        price = obj.product.discounted_price
        total = price * obj.quantity
        return f"{total} UZS"

    get_total_price.short_description = "Total Price"




@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'get_products', 'created_at', 'updated_at']
    search_fields = ['title']
    ordering = ['title']
    date_hierarchy = 'created_at'

    def get_products(self,obj):
        return obj.products.count()

    get_products.short_description = 'All Products'



@admin.register(Product)
class ProductAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'price',
        'discount',
        'get_discounted_price',
        'category',
        'stock',
        'in_stock',
        'my_order',
        'get_image',
        'created_at',
        'updated_at'
    ]

    list_filter = [
        'category',
        'discount',
        'stock',
        'updated_at',
        'created_at',
    ]

    search_fields = ['name', 'description']

    ordering = ['my_order']

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" />'.format(obj.image.url))

        return format('<img src="{}" width="80" height="80" />'.format(static('app/images/not_found_image.avif')))

    get_image.short_description = "Image"

    def in_stock(self, obj):
        return obj.stock > 0
    in_stock.boolean = True

    in_stock.short_description = "In stock"

    def get_discounted_price(self, obj):
        return f"{obj.discounted_price} usd"

    get_discounted_price.short_description = "Discounted Price"