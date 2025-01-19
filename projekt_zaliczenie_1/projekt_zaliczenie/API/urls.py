from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from.views import (
    SongViewSet,
    CreateSongView,
    BuySongView,
    UpdateASongView,
    deleteSongView,
    RegisterView,
    CustomLoginView,
) 

#router = DefaultRouter()
#router.register(r'songs', SongViewSet, basename='song')

urlpatterns = [
    #path('', include(router.urls)),  # Automatyczne ścieżki z routera
    path('songs/create/', CreateSongView.as_view()),  # Endpoint dla tworzenia piosenki
    path('songs/<int:pk>/', BuySongView.as_view()),  # Pobranie szczegółów utworu
    path('songs/<int:pk>/update/', UpdateASongView.as_view()),  # Aktualizacja utworu
    path('songs/<int:pk>/delete/', deleteSongView.as_view()),  # Usuwanie utworu
    path('register/', RegisterView.as_view(), name='register'),  # Rejestracja użytkownika
    path('login/', CustomLoginView.as_view(), name='custom_login'),  # Logowanie użytkownika
]