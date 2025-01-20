from rest_framework import serializers
from .models import Song, Album, Cart, Order, OrderAlbum
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User  
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')  
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song 
        fields = ('id', 'title', 'artist', 'album', 'release_date', 'genre')


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'release_date', 'genre']


class CartSerializer(serializers.ModelSerializer):
    album = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = ['user', 'album', 'quantity', 'added_at']

class OrderAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAlbum
        fields = ['album', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderAlbumSerializer(source='orderalbum_set', many=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'status', 'order_date', 'shipping_address', 'order_items']