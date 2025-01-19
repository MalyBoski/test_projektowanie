from django.db import models
from django.utils import timezone
from django.db.models import IntegerChoices
from django.shortcuts import render

class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    password = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    
