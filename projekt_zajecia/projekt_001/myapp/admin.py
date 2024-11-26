from django.contrib import admin

from .models import Osoba, Stanowisko, Team, Person
# Register your models here.

admin.site.register(Osoba)
admin.site.register(Stanowisko)
admin.site.register(Team)
admin.site.register(Person)