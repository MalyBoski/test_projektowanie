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
import logging
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger(__name__)
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
                "token": token.key  
            }, status=200)
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
        logger.info(f"Użytkownik: {request.user}, is_staff: {request.user.is_staff}")
        logger.info(f"Metoda: {request.method}")
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BuySongView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data) 
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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

    def post(self, request):
        logger.info(f"Typ request.user: {type(request.user)}, Wartość: {request.user}")
        
        album_id = request.data.get('album_id')
        if not album_id:
            return Response({"error": "Album ID jest wymagane"}, status=400)

        try:
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return Response({"error": "Album nie istnieje"}, status=404)

        cart_item, created = Cart.objects.get_or_create(user=request.user, album=album)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        total_cart_price = Cart.total_cart_price(request.user)

        return Response({"message": f"Dodano {album.title} do koszyka", "quantity": cart_item.quantity}, status=201)

    def get(self, request):
        user = request.user 
        cart_items = Cart.objects.filter(user=user)  
        serializer = CartSerializer(cart_items, many=True)
        total_cart_price = Cart.total_cart_price(user)  
        return Response({
            "cart_items": serializer.data,
            "total_price": total_cart_price
        }, status=200) 


def add_to_cart(request, album_id):
    album = Album.objects.get(id=album_id)
    user = User.objects.get(username=request.user)

    cart_item, created = Cart.objects.get_or_create(user=user, album=album)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


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

    def get (self, request):

        carts = Cart.objects.select_related('user', 'album').all()


        data = []
        for cart in carts:
            data.append({
                "user": cart.user.username,
                "album": cart.album.title,
                "quantity": cart.quantity, 
                "added_at": cart.added_at.strftime("%Y-%m-%d %H:%M:%S"),
                "total_price": cart.album.price * cart.quantity
            })
        return Response(data, status=200)

class PurchaseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Koszyk jest pusty!"}, status=400)

        total_price = sum(item.album.price * item.quantity for item in cart_items)

        cart_items.delete()

        return render(request, "sklepmuzyczny/thank_you.html", {"total_price": total_price})

@login_required
def create_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to create an order'}, status=403)
    
    user = request.user
    carts = Cart.objects.filter(user=user)

    if not carts.exists():
        return redirect('cart')

    total_price = sum(cart.total_price() for cart in carts)

    order = Order.objects.create(
        user=user,
        total_price=total_price,
        status=Order.Status.PENDING,  
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

    return redirect('order_detail', order_id=order.id)


def order_detail(request, order_id):
    permission_classes = [IsAuthenticated]
    order = Order.objects.get(id=order_id)
    return render(request, 'API/order_detail.html', {'order': order})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer