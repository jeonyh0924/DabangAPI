from django.contrib import admin

# Register your models here.
from members.models import User, RecentlyPostList, ContactToBroker, SocialLogin


class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'email']


class RecentlyPostListAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'post']


class ContactToBrokerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'broker']


class SocialAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type']




admin.site.register(User, UserAdmin)
admin.site.register(RecentlyPostList, RecentlyPostListAdmin)
admin.site.register(ContactToBroker, ContactToBrokerAdmin)
admin.site.register(SocialLogin, SocialAdmin)