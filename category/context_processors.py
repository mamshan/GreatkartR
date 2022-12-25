from .models import Category , SubCategory
from django.db import connection


def menu_links(request):
    
    links = Category.objects.raw('select a.id,a.slug as aslug ,  b.slug as bslug from category_category as a inner join category_subcategory   as b where b.category_id = a.id')
  
    links = SubCategory.objects.all()
    return dict(links=links)


 
def menu_links2(request):
    
    mainlinks = Category.objects.all()
    return dict(mainlinks=mainlinks)
