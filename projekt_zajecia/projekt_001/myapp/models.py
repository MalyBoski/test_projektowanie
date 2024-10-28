from django.db import models

# Create your models here.
class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=100, blank=False)
    opis = models.TextField(blank=True)  # opcjonalne pole opisu

    def __str__(self):
        return self.nazwa

class Osoba(models.Model):
    #osoba z polami imie, nazwisko, plec i stanowisko 
    plec_wybor = (
        ('K', 'Kobieta'),
        ('M', 'Mezczyzna'),
        ('I', 'Inne'),
    )
    
    imie = models.CharField(max_length=60, blank=False)
    nazwisko = models.CharField(max_length=60, blank=False)
    plec = models.CharField(max_length=1, choices=plec_wybor)
    stanowisko = models.ForeignKey(Stanowisko, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.imie} {self.nazwisko}"
    