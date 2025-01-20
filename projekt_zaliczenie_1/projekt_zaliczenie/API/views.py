from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, viewsets
from.models import Song, Album, Cart, CustomUser, Order, OrderAlbum
from.serializers import SongSerializer, CartSerializer, OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from.serializers import SongSerializer, UserSerializer, AlbumSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
# Create your views here.
class CustomLoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:

            token, created = Token.objects.get_or_create(user=user)

            songs = Song.objects.all()
            songs_serializer = SongSerializer(songs, many=True)

            return Response({
                "message": f"Witaj, {username}",
                'songs': songs_serializer.data,
                "token": token.key  }, status=200)
        return Response({"message": "Nieprawidłowe dane logowania"}, status=400)

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
    
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    model = Song
    template_name = 'sklepmuzyczny/song_list.html'
    context_object_name = 'songs'

class CreateSongView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        
class deleteSongView(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            song.delete()
            return Response({"message": "Pomyślnie usunięto utwór"}, status=204)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
           
def song_list_view(request):
    songs = Song.objects.all()
    context = {'songs': songs}
    return render(request, 'sklepmuzyczny/song_list.html', context)
    

def album_list(request):
    albums = Album.objects.all()
    return render(request, 'sklepmuzyczny/album_list.html', {'albums': albums})


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Album.objects.all()

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

        Cart.objects.create(user=user, album=album)
        return Response({"message": f"Album '{album.title}' został dodany do koszyka"}, status=201)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class AlbumsByLetterView(APIView):
    permission_classes = [IsAuthenticated]

    def get (self, request, letter):
        albums = Album.objects.filter(title__istartswith=letter)

        data =[{"id": album.id, "title": album.title, "price": album.price} for album in albums]
        return Response(data, status=200) 

class AllOrderView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        orders = Order.objects.select_related('user').all()  

        data = []
        for order in orders:
        
            order_albums = order.orderalbum_set.select_related('album').all()
            albums_data = [
                {
                    "album_title": order_album.album.title,
                    "quantity": order_album.quantity,
                    "price_per_item": float(order_album.album.price),
                    "total_price": float(order_album.album.price * order_album.quantity),
                }
                for order_album in order_albums
            ]
            
            
            data.append({
                "user": {
                    "username": order.user.username, 
                },
                "order_id": order.id,
                "status": order.get_status_display(),
                "total_price": float(order.total_price),
                "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                "shipping_address": order.shipping_address,
                "albums": albums_data,
            })

        return Response(data, status=200)



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

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'sklepmuzyczny/order_detail.html', {'order': order})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

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