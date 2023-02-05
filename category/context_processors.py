from .models import Category , SubCategory
from django.db import connection


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)