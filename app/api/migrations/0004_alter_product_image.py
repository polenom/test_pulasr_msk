# Generated by Django 4.1.4 on 2022-12-13 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_path_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.TextField(blank=True, max_length=400),
        ),
    ]
