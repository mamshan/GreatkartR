from django.contrib import admin

from category.models import Category , SubCategory

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}  # Gợi ý trường slug theo category_name
    list_display = ('category_name', 'slug', 'order_pos')

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('subcategory_name',)}  # Gợi ý trường slug theo category_name
    list_display = ('category','subcategory_name', 'slug')



# Register your models here.
admin.site.register(Category, CategoryAdmin)

admin.site.register(SubCategory, SubCategoryAdmin)