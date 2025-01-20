from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, viewsets
from.models import Song, Album, Cart, Order, OrderAlbum
from.serializers import SongSerializer, CartSerializer, OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from.serializers import SongSerializer, UserSerializer, AlbumSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
#https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
from django.contrib.auth import get_user_model
User = get_user_model()
# https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/
from django.utils import timezone
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# https://docs.djangoproject.com/en/5.1/topics/http/shortcuts/
from django.shortcuts import get_object_or_404
# https://docs.djangoproject.com/en/2.2/_modules/django/utils/dateparse/
from django.utils.dateparse import parse_date
# Create your views here.

# Wlasne wyswietlanie logowania wyrzucenie wiadomosci i tokenu po zalogowaniu
class CustomLoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:

            token, created = Token.objects.get_or_create(user=user) 

            return Response({
                "message": f"Witaj, {username}",
                "token": token.key  }, status=200)
        return Response({"message": "Nieprawidłowe dane logowania"}, status=400)
# Wyswietlanie rejestracji uzytkownika
class RegisterView(APIView):
    permission_classes = []
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
              {"message": "Użytkownik został zarejestrowany pomyślnie"},
              status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Glowna strona z albumami
class MainPageView(APIView):
    permission_classes = []
    
def main_page_view(request):
        albums = Album.objects.prefetch_related('song_set').all()
        context = {'albums': albums}
        return render(request, 'sklepmuzyczny/main_page.html', context)


# Tworzenie piosenek
class CreateSongView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Updateowanie piosenek 
class UpdateASongView(APIView):
    permission_classes = [IsAdminUser]
    def put(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Pomyślnie zaktualizowano utwór"}, status=200)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
# Usuwanie piosenek
class deleteSongView(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            song.delete()
            return Response({"message": "Pomyślnie usunięto utwór"}, status=204)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
# Wyswietlanie listy piosenek
def song_list_view(request):
    songs = Song.objects.all()
    context = {'songs': songs}
    return render(request, 'sklepmuzyczny/song_list.html', context)
    

def album_list(request):
    albums = Album.objects.all()
    return render(request, 'sklepmuzyczny/album_list.html', {'albums': albums})

# Wyswietlanie albumow 
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Album.objects.all()
# Wyswietlanie koszyka
class CartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total_price = sum(item.album.price for item in cart_items)

        return Response({
            "cart_items": [{"album": item.album.title, "price": item.album.price} for item in cart_items],
            "total_price": total_price
        }, status=200)
# Wyswietlanie dodawania do koszyka
class AddToCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        album_name = request.data.get("name")

        if not album_name:
            return Response({"error": "Nazwa albumu jest wymagana"}, status=400)

        try:
            album = Album.objects.get(title=album_name)
        except Album.DoesNotExist:
            return Response({"error": "Nie znaleziono albumu"}, status=404)

        cart_item, created = Cart.objects.get_or_create(user=user, album=album)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_items = Cart.objects.filter(user=user)
        total_cart_price = sum(item.album.price * item.quantity for item in cart_items)

        cart_data = [
            {
                "album": item.album.title,
                "price": item.album.price,
                "quantity": item.quantity
            }
            for item in cart_items
        ]

        return Response({
            "message": f"Album '{album.title}' został dodany do koszyka",
            "cart_items": cart_data,
            "total_price": total_cart_price
        }, status=200)


# Dodawanie do koszyka
def add_to_cart(request, name):
    album = Album.objects.get(title=name)
    user = User.objects.get(username=request.user)

    cart_item, created = Cart.objects.get_or_create(user=user, album=album)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

# Wyswietlanie dla biedakow

class DlaBiedakow(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        cheap_albums = Album.objects.filter(price__lt=20)

        data = [{"id": album.id, "title": album.title, "price": album.price} for album in cheap_albums]
        return Response(data, status=200)


# Wyswietlanie albumow po literze

class AlbumsByLetterView(APIView):
    permission_classes = [IsAuthenticated]

    def get (self, request, letter):
        albums = Album.objects.filter(title__istartswith=letter)

        data =[{"id": album.id, "title": album.title, "price": album.price} for album in albums]
        return Response(data, status=200) 
# Wyswietlanie wszystkich zamowien
class AllOrderView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        orders = Order.objects.select_related('user').all()
        if start_date:
            orders = orders.filter(order_date__gte=parse_date(start_date))
        if end_date:
            orders = orders.filter(order_date__lte=parse_date(end_date))

        return render(request, 'orders_list.html', {'orders': orders})


# Wyswietlanie zamowienia
class PurchaseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        order = Order.objects.filter(user=user, status="PENDING").first()

        if not order:
            return Response({"error": "Brak otwartego zamówienia do przetworzenia"}, status=400)

        order.status = "COMPLETED" 
        order.save()

        return Response({
            "message": "Zakup zakończony pomyślnie",
            "order_id": order.id,
            "total_price": float(order.total_price),
            "status": order.status
        }, status=200)



class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        carts = Cart.objects.filter(user=user)

        if not carts.exists():
            return Response({"error": "Koszyk jest pusty!"}, status=400)

        total_price = sum(cart.album.price * cart.quantity for cart in carts)

        order = Order.objects.create(
            user=user,
            total_price=total_price,
            status="PENDING",
            order_date=timezone.now(),
            shipping_address=request.data.get('shipping_address', ''),
        )

        for cart in carts:
            OrderAlbum.objects.create(
                order=order,
                album=cart.album,
                quantity=cart.quantity,
            )

        carts.delete()

        return Response({"message": "Zamówienie zostało utworzone", "order_id": order.id}, status=201)
# Szczegoly zamowienia
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'sklepmuzyczny/order_detail.html', {'order': order})
# Wyswietlanie zamowien

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
# OSTATNIE ZAMOWIENIE
class LastOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        last_order = Order.objects.filter(user=user).order_by('-order_date').first()
        
        if not last_order:
            return Response({"error": "Nie znaleziono zamówień"}, status=404)

        return Response({
            "order_id": last_order.id,
            "status": last_order.get_status_display(),
            "total_price": float(last_order.total_price),
            "order_date": last_order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "shipping_address": last_order.shipping_address,
        }, status=200)
# USEROWE ZAMOWIENIE :O?
class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user).order_by('-order_date')
        
        if not orders.exists():
            return Response({"error": "Nie znaleziono zamówień"}, status=404)

        data = [
            {
                "order_id": order.id,
                "status": order.get_status_display(),
                "total_price": float(order.total_price),
                "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                "shipping_address": order.shipping_address,
            }
            for order in orders
        ]
        return Response(data, status=200)   