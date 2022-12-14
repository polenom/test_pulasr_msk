import os

from PIL import Image
from rest_framework.serializers import ModelSerializer, ChoiceField, ImageField, CharField, Field, StringRelatedField

from api.models import Product, FormatImage
from django.conf import settings
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from api.services import create_url


class ProductStatusChoiceSerializer(ChoiceField):
    def to_representation(self, value):
        return self.choices[value].label


    # def to_internal_value(self, data):
    #     if data == '' and self.allow_blank:
    #         return ''
    #
    #     try:
    #         return self.get_key(data)
    #     except KeyError:
    #         self.fail('invalid_choice', input=data)
    #
    # def get_key(self, date):
    #     for key in self.choices:
    #         print(self.choices[key].label)
    #         if self.choices[key].label == date:
    #             return key
    #     raise KeyError

class ImageSerializer(ImageField):

    def to_representation(self, value):
        return {"path": f"/media/{value}", }


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Пример',
            summary='first',
            description='Пример',
            value={
                'title': 'box',
                'cost': 123,
                'articl': 1233123,
                'statuc': 'в наличии',
                'image': {
                    'path' :['/name_file'],
                    'formats': [
                        'png',
                        'webp'
                    ]
                }
            }
        )
    ]
)
class ProductSerializer(ModelSerializer):
    status = ProductStatusChoiceSerializer(choices=Product.StatusChoices, read_only=False)
    image = ImageSerializer(required=False)
    formats = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'articl', 'cost', 'status', 'image', 'formats')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        file_data = self.splite_filename(validated_data)
        instance_product = Product.objects.create(**validated_data)
        self.make_file(file_data, instance_product)
        return instance_product

    def update(self, instance, validated_data):
        file_data = self.splite_filename(validated_data)
        for key in validated_data:
            setattr(instance, key, validated_data[key])
        instance.save()
        self.make_file(file_data, instance)
        return instance

    def add_ext(self, extends: list[str], obj: "Product") -> None:
        if not extends:
            return None
        all_formats = {i.name: i for i in obj.formats.all()}
        all_new_formats = []
        for ext in extends:
            if all_formats.get(ext, None):
                del all_formats[ext]
            else:
                inst, _ = FormatImage.objects.get_or_create(name=ext)
                all_new_formats.append(inst)
        obj.formats.add(*all_new_formats)
        obj.formats.remove(*all_formats.values())

    def splite_filename(self, validated_data) -> tuple | None:
        file = validated_data.pop('image', None)
        if file:
            filename, extend = os.path.splitext(file.name)
            url = create_url(filename)
            validated_data['image'] = url
            return (url, extend, file)

    def make_file(self, splite_filename: tuple | None, instance_product) -> None:
        if splite_filename:
            filename, extend, file = splite_filename
            extend_list = []
            file_path = f'{settings.MEDIA_ROOT}/{filename + extend}'
            self.save_file_on_disc(file, file_path)
            extend_list.append(extend[1:])
            if self.check_formats(extend):
                self.convert_to_webp(file_path, filename)
                extend_list.append('webp')
            self.add_ext(extend_list, instance_product)

    def save_file_on_disc(self, file: "InMemoryUploadedFile", path: str) -> None:
        with open(path, 'wb') as f:
            for fragment in file.chunks():
                f.write(fragment)

    def check_formats(self, ext: 'str') -> bool:
        return ext in {'.png', '.jpg', 'png', 'jpg'}

    def convert_to_webp(self, path: 'str', filename: 'str') -> None:
        image = Image.open(path)
        image.save(f'{settings.MEDIA_ROOT}/{filename + ".webp"}', format='webp')

    def to_representation(self, instance):
        date = super().to_representation(instance)
        date['image']['formats'] = date.pop('formats', [])
        return date
