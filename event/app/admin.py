from django.contrib import admin

# Register your models here.
from .models import Vendor_Registration, Product,User_Registration

class VendorAdmin(admin.ModelAdmin):
    list_display = ( "username", "email")

class ProductAdmin(admin.ModelAdmin):
    list_display = ("vendor", "name")

class UserAdmin(admin.ModelAdmin):
    list_display=("username","email")
# Register each model separately
admin.site.register(Vendor_Registration, VendorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(User_Registration, UserAdmin)
