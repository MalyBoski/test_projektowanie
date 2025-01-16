from django.contrib import admin
from .models import Stanowisko, Osoba, Produkt, User, Song

class OsobaAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'stanowisko_with_id', 'data_dodania', 'miesiac', 'plec']
    list_filter = ['stanowisko', 'data_dodania', 'miesiac'] 

    @admin.display(description='Stanowisko (ID)')
    def stanowisko_with_id(self, obj):
        if obj.stanowisko:
            return f'{obj.stanowisko.nazwa} ({obj.stanowisko.id})'
        return "Brak stanowiska"
    list_filter = ["stanowisko", "data_dodania"]

class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'album', 'release_date', 'genre']
    list_filter = ['title', 'artist', 'album', 'release_date', 'genre']
    
class StanowiskoAdmin(admin.ModelAdmin):
    list_display = ["nazwa", "opis"]
    list_filter = ["nazwa"]
admin.site.register(Stanowisko, StanowiskoAdmin) 
admin.site.register(Produkt)
admin.site.register(User)
admin.site.register(Osoba, OsobaAdmin)
admin.site.site_header = "Panel administracyjny"
admin.site.site_title = "Panel administracyjny"
admin.site.register(Song, SongAdmin)