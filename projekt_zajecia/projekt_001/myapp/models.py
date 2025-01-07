from django.db import models

# Create your models here.
# deklaracja statycznej listy wyboru do wykorzystania w klasie modelu
MONTHS = models.IntegerChoices('Miesiace', 'Styczeń Luty Marzec Kwiecień Maj Czerwiec Lipiec Sierpień Wrzesień Październik Listopad Grudzień')

SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )


class Stanowisko(models.Model):
    nazwa = models.CharField(max_length=100, blank=False)
    verbose_name = 'Stanowisko'
    verbose_name_plural = 'Stanowiska'
    opis = models.TextField(blank=True)  # opcjonalne pole opisu

    def __str__(self):
        return self.nazwa
    
    class Meta:
        verbose_name = 'Stanowisko'
        verbose_name_plural = 'Stanowiska'

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
    rozmiar_koszulki = models.CharField(max_length=1, choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    miesiac_dodany = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])


    def __str__(self):
        return f"{self.imie} {self.nazwisko}"
    
    class Meta:
        verbose_name = 'Osoba'
        verbose_name_plural = 'Osoby'
    
    

class Team(models.Model):
    name = models.CharField(max_length=60)
    panstwo = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Zespół'
        verbose_name_plural = 'Zespoły'


class Person(models.Model):

    pseudonim = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=60)
    rozmiar_koszulki = models.CharField(max_length=1, choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    month_added = models.IntegerField(choices=MONTHS.choices, default=MONTHS.choices[0][0])
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Osobatest'
        verbose_name_plural = 'Osobytest'