from rest_framework import serializers
from django.contrib.auth.models import User
from bangazon_api.models import Store
from bangazon_api.models.favorite import Favorite

class StoreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class StoreSerializer(serializers.ModelSerializer):
    seller = StoreUserSerializer()

    class Meta:
        model = Store
        fields = ('id', 'name', 'description', 'seller', 'products')
        depth = 1


class AddStoreSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()

class FavoriteStoreSerializer(serializers.Serializer):
    store = StoreSerializer()

    class Meta:
        model = Favorite
        fields = ('store')
