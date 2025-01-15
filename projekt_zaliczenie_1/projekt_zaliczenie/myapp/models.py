from django.db import models
from django.utils import timezone
from django.db.models import IntegerChoices
from django.shortcuts import render
# Create your models here.

MONTHS = models.IntegerChoices('Miesiace', 'Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień')
# deklaracja statycznej listy wyboru do wykorzystania w klasie modelu
SHIRT_SIZES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
]

class plec(IntegerChoices): 
    mezczyzna = 1, 'Mężczyzna'
    kobieta = 2, 'Kobieta'
    inne = 3, 'Inne'


class Osoba(models.Model): 
    pseudonim = models.CharField(max_length=100, default="")
    imie = models.CharField(max_length=60, blank=False)
    nazwisko = models.CharField(max_length=60, blank=False)
    plec = models.IntegerField(choices=plec.choices)
    stanowisko = models.ForeignKey('Stanowisko', on_delete=models.CASCADE)
    data_dodania = models.DateTimeField(default=timezone.now)
    miesiac = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"
    
    class Meta:
        ordering = ["nazwisko"] # jesli chcemy sortowac odwrotnie do alfabetycznie to -nazwisko
        verbose_name_plural = "Osoby"

class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=60, blank=False)
    opis = models.TextField(max_length=60, blank=True)
    def __str__(self):
        return self.nazwa
    
    class Meta:
        verbose_name_plural = "Stanowiska"
    


class Produkt(models.Model):
    name = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Produkty'

class User(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    password = models.CharField(max_length=60)
    def __str__(self):
        return self.name
    
def osoba_list(request):
    osoby=Osoba.objects.all()
    return render(request, 'myapp/osoba_list.html', {'osoby': osoby})