from rest_framework import serializers
from home.models import *

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

class OnlyproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class StoreProductSerializer(serializers.ModelSerializer):
    store = OnlyproductSerializer(many=True)
    class Meta:
        model = Store
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        depth = 1