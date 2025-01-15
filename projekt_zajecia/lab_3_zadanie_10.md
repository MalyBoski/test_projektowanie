Zadanie 1
```python
In [4]: from myapp.models import Osoba

In [5]: osoby = Osoba.objects.all

In [6]: osoby = Osoba.objects.all()

In [7]: print(osoby)
```

Zadanie 2 
```python
In [8]: osoba = Osoba.objects.get(id=3)

In [9]: print(osoba)

```

Zadanie 3 
```python
In [10]: osoba_z_K = Osoba.objects.filter(imie__startswith = 'K')

In [11]: print(osoba_z_K)

```

Zadanie 4
```python
In [12]: stanowiska = Osoba.objects.values('stanowisko').distinct()

In [13]: print(stanowiska)
```

Zadanie 5
```python
In [21]: Stanowisko.objects.values_list('nazwa', flat = True).order_by("-nazwa")
```

Zadanie 6
```python
Osoba.objects.create(
    ...: imie = 'Jan',
    ...: nazwisko = 'Kowalski',
    ...: plec = 2,
    ...: stanowisko = Stanowisko.objects.get(id = 1)
    ...: )
```