from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from.views import SongList, CreateSongView, BuySongView, UpdateASongView, deleteSongView, SongViewSet


router = DefaultRouter()
router.register(r'songs', SongViewSet, basename='song')

urlpatterns = [
    path('', include(router.urls)),
    path('songs/', SongList.as_view(), name='song-list'),
    path('songs/create/', CreateSongView.as_view()),
    path('songs/<int:pk>/', BuySongView.as_view()),
    path('songs/<int:pk>/update/', UpdateASongView.as_view()),
    path('songs/<int:pk>/delete/', deleteSongView.as_view()),
    path('songs/', SongViewSet.as_view({'get': 'list'})),
]