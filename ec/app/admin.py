from django.contrib import admin
from .models import Product,Profilee,cart,Payment,OrderPlaced,Wishlist

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']


@admin.register(Profilee)
class ProfileAdmin(admin.ModelAdmin):
   list_display=['id','user','locality','city','state','zipcode']

@admin.register(cart)
class cartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','paid','razorpay_payment_id']

@admin.register(OrderPlaced)
class cartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','quantity','ordered_date','status','payment']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product']