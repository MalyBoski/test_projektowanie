from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.db.models import IntegerChoices
from django.shortcuts import render

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    release_date = models.DateField(default=now)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.title} by {self.artist}"

class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    password = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default=1)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts') 
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name}'s cart - {self.album.title} x{self.quantity}"

    def total_price(self):
        return self.album.price * self.quantity 