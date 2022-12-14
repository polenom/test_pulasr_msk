import os.path

from django.db import models


class FormatImage(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    class StatusChoices(models.TextChoices):
        i = 'i', 'в наличии'
        o = 'o', 'под заказ'
        r = 'r', 'ожидается поступление'
        a = 'a', 'нет в наличие'
        p = 'p', 'не производит'

    title = models.CharField(max_length=255, unique=True)
    articl = models.IntegerField(unique=True)
    cost = models.FloatField(default=-1)  # -1 == нет цены на товар
    status = models.CharField(max_length=1, choices=StatusChoices.choices)
    image = models.TextField(max_length=400, blank=True)
    formats = models.ManyToManyField(FormatImage)




