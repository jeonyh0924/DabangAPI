from django.contrib import admin

# Register your models here.
from presales.models import PreSale, PreSaleImage, Thema, Brand


class PreSaleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'thema']


class PreSaleImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'presale', 'image']


class ThemaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', ]


class BrandAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


admin.site.register(PreSale, PreSaleAdmin)
admin.site.register(PreSaleImage, PreSaleImageAdmin)
admin.site.register(Thema, ThemaAdmin)
admin.site.register(Brand, BrandAdmin)