from rest_framework import serializers
from django.utils.text import slugify
from .models import Product
from application.utils.bucket import BucketClient


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.ImageField(write_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        image_url = self.__update_image_url(validated_data)
        validated_data['image_url'] = image_url
        record = Product(**validated_data)
        record.save()
        return record

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'image_url':
                image_url = self.__update_image_url(validated_data)
                instance['image_url'] = image_url
            else:
                setattr(instance, attr, value)

        instance.save()
        return validated_data

    def delete(self, instance):
        instance.status = False
        instance.save()
        return instance

    def __update_image_url(self, validated_data):
        image = validated_data['image_url']
        name = validated_data['name']

        bucket_client = BucketClient('products')

        return bucket_client.upload_object(
            f'{slugify(name)}.png', image.file
        )
