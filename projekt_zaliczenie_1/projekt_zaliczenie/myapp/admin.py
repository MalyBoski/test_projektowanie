from django.contrib import admin
from .models import Stanowisko, Osoba, Produkt, User
# Register your models here.
class OsobaAdmin(admin.ModelAdmin):
    list_display = ['imie', 'nazwisko', 'stanowisko', 'data_dodania', 'miesiac']
    list_filter = ['stanowisko', 'data_dodania', 'miesiac']

admin.site.register(Stanowisko) 
admin.site.register(Produkt)
admin.site.register(User)
admin.site.register(Osoba, OsobaAdmin)