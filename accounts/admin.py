from django.contrib import admin

from accounts.models import Account, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'username', 'first_name', 'last_name')   # Các trường có gắn link dẫn đến trang detail
    readonly_fields = ('last_login', 'date_joined')     # Chỉ cho phép đọc
    ordering = ('-date_joined',)     # Sắp xếp theo chiều ngược

    # Bắt buộc phải khai báo
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self , object):
        return format_html(
            '<img src="{}" width="30" style="border-radius:50%;">' . format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'    
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')
    

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

