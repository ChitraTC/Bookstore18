from django.contrib import admin
from .models import Book, Customer, Cart


# Register your models here.


# admin.site.register(Book)
@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','author','price','category','image_url','book_available']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']
#
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','book','quantity']