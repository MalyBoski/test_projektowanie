from django.contrib import admin
from .models import User, Song, Album, Cart

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_date', 'genre']
    list_filter = ['artist', 'release_date', 'genre']

class SongAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'artist', 'album', 'release_date', 'genre']
    list_filter = ['id','title', 'artist', 'album', 'release_date', 'genre']
    
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'quantity', 'added_at') 
    list_filter = ('user', 'album') 
    search_fields = ('user__name', 'album__title')

admin.site.register(User)
admin.site.site_header = "Panel administracyjny"
admin.site.site_title = "Panel administracyjny"
admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Cart, CartAdmin)