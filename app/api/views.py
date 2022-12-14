from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser

from api.models import Product
from api.serializer import ProductSerializer

from api.services import ProductFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser,FormParser, JSONParser)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    @extend_schema(
        description='Получить список продуктов с фильтрами',
        summary='Получить список продуктов с фильтрами',
        responses={200: ProductSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description='Создание нового продукта',
        summary='Cоздание нового продукта',
        responses={201: ProductSerializer(many=False),
                   400: None}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description='Получить продукт',
        summary='Получить продукт',
        responses={201: ProductSerializer(many=False),
                   404: None}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description='Удалить продукт',
        summary='Удалить продукт',
        responses={204: None,
                   404: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        description='Изменение продукта',
        summary='Изменение продукта',
        responses={200: ProductSerializer(many=False),
                   404: None}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)







