from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from music.models import Song
from music.serializers import SongSerializer
from recommender.song_analysis import recommend

class SongRecommender(APIView):
    def get(self, request, song_id):
        # get the song from the database
        song = get_object_or_404(Song, id=song_id)
        # get the lyrics of the song
        lyrics = song.lyrics
        # call the recommend function
        recommended_songs = recommend(lyrics)[:5]
        # serializer needs to be done
        print(recommended_songs)
        x = []
        for i in recommended_songs:
            song = Song.objects.get(id=i[0])
            x.append(song)

        serializer = SongSerializer(x, many=True)
        return Response(serializer.data)
        
