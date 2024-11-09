from rest_framework import serializers
from .models import User

# Uso de serializadores independientes
# class UserListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(read_only=True)
#     email = serializers.EmailField(read_only=True)
#     first_name = serializers.CharField(read_only=True)
#     last_name = serializers.CharField(read_only=True)


# class UserCreateSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     # quiero prohibir la palabra carlos, en el username
#     def validate_username(self, value):
#         # validaciones personalizadas
#         if 'carlos' in value:
#             raise serializers.ValidationError(
#                 'La palabra carlos esta prohibida.'
#             )
#         return value

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         record = User(**validated_data)
#         record.set_password(password)
#         record.save()
#         return record


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name', 'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return validated_data
