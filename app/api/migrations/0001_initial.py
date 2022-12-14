# Generated by Django 4.1.4 on 2022-12-13 12:29

import api.services
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormatImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('articl', models.IntegerField(unique=True)),
                ('cost', models.FloatField(default=-1)),
                ('status', models.CharField(choices=[('i', 'в наличии'), ('o', 'под заказ'), ('r', 'ожидается поступление'), ('a', 'нет в наличие'), ('p', 'не производит')], max_length=1)),
                ('image', models.ImageField(blank=True, upload_to=api.services.create_url)),
                ('formats', models.ManyToManyField(to='api.formatimage')),
            ],
        ),
    ]
