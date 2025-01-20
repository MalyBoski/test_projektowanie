from django.contrib import admin
from .models import CustomUser, Song, Album, Cart, Order, OrderAlbum
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from rest_framework.authtoken.models import Token

class TokenAdmin(admin.ModelAdmin):
    list_display = ('key','pk', 'user_username', 'user_id', 'is_superuser', 'created')

    def user_username(self,obj):
        return obj.user.username if obj.user else 'Brak uzytkownika'
    user_username.short_description = 'User'

    def user_id(self, obj):
        return obj.user.id if obj.user else 'Brak ID'
    user_id.short_description = 'User ID'

    def is_superuser(self,obj):
        return obj.user.is_superuser
    is_superuser.boolean = True

    def created(self,obj):
        return obj.created


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['id']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

class AlbumAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'artist', 'release_date', 'genre']
    list_filter = ['id','artist', 'release_date', 'genre']

class SongAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'artist', 'album', 'release_date', 'genre']
    list_filter = ['id','title', 'artist', 'album', 'release_date', 'genre']
    
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'quantity', 'added_at') 
    list_filter = ('user', 'album') 
    search_fields = ('user__name', 'album__title')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'order_date')
    list_filter = ('status',)
    search_fields = ('user__username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.site_header = "Panel administracyjny"
admin.site.site_title = "Panel administracyjny"
admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Cart, CartAdmin)   
admin.site.register(Token, TokenAdmin)