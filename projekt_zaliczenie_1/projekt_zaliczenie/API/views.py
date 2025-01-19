from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from.models import Song, Album, Cart
from.serializers import SongSerializer, CartSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from.serializers import SongSerializer, UserSerializer, AlbumSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from rest_framework.permissions import IsAdminUser, IsAuthenticated
import logging
logger = logging.getLogger(__name__)
# Create your views here.
class CustomLoginView(APIView):
    permission_classes = [IsAuthenticated]

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
                'songs': songs_serializer.data
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
    def get(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data) 
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UpdateASongView(APIView):
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
    album_data = [{"id": album.id, "name": album.name, "artist": album.artist} for album in albums]
    return JsonResponse(album_data, safe=False)


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Album.objects.all()

@login_required
def cart_view(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    return render(request, 'cart.html', {'cart_items': cart_items})


def add_to_cart(request, album_id):
    album = Album.objects.get(id=album_id)
    user = request.user

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