from django.contrib import admin
from .models import *
# Register your models here.

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'namamaterial', 'date_created', 'is_active', 'created_by')

class KategoriAdmin(admin.ModelAdmin):
    list_display = ('id', 'namakategori', 'is_active')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'namaproduct', 'kategori', 'is_active')

admin.site.register(Material, MaterialAdmin)
admin.site.register(Kategori, KategoriAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Pengguna)