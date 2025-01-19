from django.contrib import admin
from .models import User, Song

class SongAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'artist', 'album', 'release_date', 'genre']
    list_filter = ['id','title', 'artist', 'album', 'release_date', 'genre']
    
admin.site.register(User)
admin.site.site_header = "Panel administracyjny"
admin.site.site_title = "Panel administracyjny"
admin.site.register(Song, SongAdmin)