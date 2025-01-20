from django.urls import path 
from.views import CreateSongView, UpdateASongView, deleteSongView, RegisterView, CustomLoginView, CartView, AlbumsByLetterView, AllOrderView, PurchaseView, CreateOrderView, OrderDetailView, main_page_view, song_list_view, DlaBiedakow, UserOrdersView, LastOrderView, AddToCartView
from . import views

urlpatterns = [
    path('orders/user/', UserOrdersView.as_view(), name='user_orders'),
    path('order/last/', LastOrderView.as_view(), name='last_order'),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/purchase/', PurchaseView.as_view(), name="order-purchase"),
    path('cart/', CartView.as_view(), name='cart'), 
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('albums/', views.album_list, name='album_list'),
    path('albums/by-letter/<str:letter>/', AlbumsByLetterView.as_view(), name='albums-by-letter'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('main/', main_page_view, name='main_page'),  
    path('songs/', song_list_view, name='song_list'),
    path('dlabiedakow/', DlaBiedakow.as_view(), name='dlabiedakow'),
    # Admin opcje
    # Mozliwosc wybierania zamowien z okreslonej daty
    # http://127.0.0.1:8000//API/orders/all/?start_date=rok-miesiac-dzien&end_date=rok-miesiac-dzien    (np. 2023-01-31)
    path('orders/all/', AllOrderView.as_view(), name='all-orders'), 
    path('songs/create/', CreateSongView.as_view()),
    path('songs/<int:pk>/update/', UpdateASongView.as_view()),
    path('songs/<int:pk>/delete/', deleteSongView.as_view()),
]