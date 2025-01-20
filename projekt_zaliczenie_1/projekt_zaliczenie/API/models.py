from django.db import models
from django.utils import timezone
from django.utils.timezone import now
# https://docs.djangoproject.com/en/5.1/topics/settings/
from django.conf import settings 
# https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
from django.contrib.auth.models import AbstractUser
class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    release_date = models.DateField(default=now)
    genre = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.title} by {self.artist}"

class CustomUser(AbstractUser):
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts') 
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.album.title} x{self.quantity}"


    def total_price(self):
        return self.album.price * self.quantity 
    
    @classmethod
    def total_cart_price(cls, user):
        carts = cls.objects.filter(user=user)
        return sum(cart.total_price() for cart in carts)

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    album = models.ManyToManyField(Album, through='OrderAlbum')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    order_date = models.DateTimeField(default=timezone.now)
    shipping_address = models.CharField(max_length=255)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"

    def update_total_price(self):
        total = sum(order_album.album.price * order_album.quantity for order_album in self.orderalbum_set.all())
        self.total_price = total
        self.save()


class OrderAlbum(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.album.title} x{self.quantity} for Order {self.order.id}"