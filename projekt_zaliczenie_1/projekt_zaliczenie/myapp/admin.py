from django.contrib import admin
from .models import Stanowisko, Osoba, Produkt, User

class OsobaAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'stanowisko_with_id', 'data_dodania', 'miesiac', 'plec']
    list_filter = ['stanowisko', 'data_dodania', 'miesiac'] 

    @admin.display(description='Stanowisko (ID)')
    def stanowisko_with_id(self, obj):
        if obj.stanowisko:
            return f'{obj.stanowisko.nazwa} ({obj.stanowisko.id})'
        return "Brak stanowiska"
    list_filter = ["stanowisko", "data_dodania"]
class StanowiskoAdmin(admin.ModelAdmin):
    list_display = ["nazwa", "opis"]
    list_filter = ["nazwa"]
admin.site.register(Stanowisko, StanowiskoAdmin) 
admin.site.register(Produkt)
admin.site.register(User)
admin.site.register(Osoba, OsobaAdmin)