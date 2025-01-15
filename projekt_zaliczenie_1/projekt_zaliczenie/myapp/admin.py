from django.contrib import admin
from .models import Stanowisko, Osoba, Produkt, User
# Register your models here.
class OsobaAdmin(admin.ModelAdmin):
    readonly_fields = ('data_dodania',)

admin.site.register(Osoba)
admin.site.register(Stanowisko) 
admin.site.register(Produkt)
admin.site.register(User)