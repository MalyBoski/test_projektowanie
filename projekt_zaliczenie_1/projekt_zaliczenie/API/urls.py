from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from.views import SongList, CreateSongView, UpdateASongView, deleteSongView, SongViewSet, RegisterView, CustomLoginView, CartView, AlbumViewSet, AlbumsByLetterView, AllOrderView, PurchaseView, CreateOrderView, OrderDetailView
from . import views

urlpatterns = [
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('cart/purchase/', PurchaseView.as_view(), name="cart-purchase"),
    path('cart/', CartView.as_view(), name='cart'), 
    path('cart/add/', CartView.as_view(), name='add_to_cart'),
    path('albums/', views.album_list, name='album_list'),
    path('orders/all/', AllOrderView.as_view(), name='all-orders'),
    path('albums/by-letter/<str:letter>/', AlbumsByLetterView.as_view(), name='albums-by-letter'),
    path('songs/', SongList.as_view(), name='song-list'),
    path('songs/create/', CreateSongView.as_view()),
    path('songs/<int:pk>/update/', UpdateASongView.as_view()),
    path('songs/<int:pk>/delete/', deleteSongView.as_view()),
    path('songs/', SongViewSet.as_view({'get': 'list'})),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),    
]