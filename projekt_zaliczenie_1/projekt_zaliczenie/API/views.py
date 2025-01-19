from django.shortcuts import render
from rest_framework import generics, viewsets
from.models import Song
from.serializers import SongSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from.serializers import SongSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
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
    def post(self, request):
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
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class deleteSongView(APIView):
    def delete(self, request, pk):
        try:
            song = Song.objects.get(pk=pk)
            song.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
           
def song_list_view(request):
    songs = Song.objects.all()
    context = {'songs': songs}
    return render(request, 'sklepmuzyczny/song_list.html', context)
    
