# Generated by Django 4.0.4 on 2023-02-16 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subimgs',
            field=models.ImageField(default='', upload_to='photos/products'),
            preserve_default=False,
        ),
    ]