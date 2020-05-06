from django.contrib import admin

from posts.models import SalesForm, PostAddress, SecuritySafetyFacilities, PostRoom, AdministrativeDetail, \
    MaintenanceFee, RoomOption, RoomSecurity, Broker, PostImage, OptionItem, ComplexInformation, ComplexImage, \
    RecommendComplex, PostLike


# Register your models here.


class PostRoomAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type', 'parkingDetail', 'parkingTF', 'parkingPay', 'complex']


class SalesFormAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type', 'depositChar', 'monthlyChar', 'depositInt', 'monthlyInt', ]


class AdministrativeDetailAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', ]


class PostAddressAdmin(admin.ModelAdmin):
    list_display = ['pk', 'loadAddress']


class SecuritySafetyFacilitiesAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'image']


class MaintenanceFeeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'postRoom', 'admin', 'totalFee']


class RoomOptionAdmin(admin.ModelAdmin):
    list_display = ['pk']


class RoomSecurityAdmin(admin.ModelAdmin):
    list_display = ['pk']


class BrokerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'companyName', 'address', 'managerName', 'tel', 'image']


class PostImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'post', 'image']


class OptionItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'image']


class PostLIkeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', ]


class ComplexInformationAdmin(admin.ModelAdmin):
    list_display = ['pk', 'complexName', 'constructionCompany', ]


class ComplexImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'image', 'complex', ]


class RecommendComplexAdmin(admin.ModelAdmin):
    list_display = ['pk', 'image', 'complex']


admin.site.register(PostRoom, PostRoomAdmin)
admin.site.register(SalesForm, SalesFormAdmin)
admin.site.register(PostAddress, PostAddressAdmin)
admin.site.register(SecuritySafetyFacilities, SecuritySafetyFacilitiesAdmin)

admin.site.register(AdministrativeDetail, AdministrativeDetailAdmin)
admin.site.register(MaintenanceFee, MaintenanceFeeAdmin)
admin.site.register(RoomOption, RoomOptionAdmin)
admin.site.register(RoomSecurity, RoomSecurityAdmin)
admin.site.register(Broker, BrokerAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(OptionItem, OptionItemAdmin)
admin.site.register(PostLike, PostLIkeAdmin)

admin.site.register(ComplexInformation, ComplexInformationAdmin)
admin.site.register(ComplexImage, ComplexImageAdmin)
admin.site.register(RecommendComplex, RecommendComplexAdmin)
