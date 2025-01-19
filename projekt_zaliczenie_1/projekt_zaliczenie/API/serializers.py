from rest_framework import serializers
from .models import User, Song
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')  # Poprawne pobieranie emaila
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song 
        fields = ('id', 'title', 'artist', 'album', 'release_date', 'genre')


# serializer z koszyka i albumu

