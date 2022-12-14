import datetime
from django_filters import rest_framework as filters
from api.models import Product

def create_url(filename: str) -> str :
    filename_out_space = filename.strip().replace(' ','')
    time_now = datetime.datetime.utcnow()
    str_time = time_now.strftime("%m-%d-%y-%H:%M:%S")
    return f'{filename_out_space}-{str_time}'


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

StatusChoices = (
        ('i', 'в наличии'),
        ('o', 'под заказ'),
        ('r', 'ожидается поступление'),
        ('a', 'нет в наличие'),
        ('p', 'не производит'),
    )

class ProductFilter(filters.FilterSet):
    articl = filters.RangeFilter()
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=StatusChoices)

    class Meta:
        model = Product
        fields = ['articl', 'title', 'status']