from email.headerregistry import Group
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin
from .models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist  
from django.contrib.auth.models import Group


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_link', 'quantity', 'total_cost']  
    def product_link(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.id])  # Ensure 'product' is the correct field
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
    product_link.short_description = "Product"  


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customers', 'products', 'quantity', 'ordered_date', 'status', 'payments']
    def customers(self,obj):
        link =reverse("admin:app_customer_change",args=[obj.customer.id])
        return format_html('<a href="{}">{}</a>',link,obj.customer.title)
    
    def products(self,obj):
        link =reverse("admin:app_product_change",args=[obj.product.id])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    
    def payments(self,obj):
        link =reverse("admin:app_payment_change",args=[obj.payment.id])
        return format_html('<a href="{}">{}</a>',link,obj.payment.razorpay_payment_id)

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products']
    def products(self,obj):
        link =reverse("admin:app_product_change",args=[obj.product.id])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    
admin.site.unregister(Group)