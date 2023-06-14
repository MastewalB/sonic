from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from music.models import Song
from music.serializers import SongSerializer
from recommender.song_analysis import recommend

class SongRecommender(APIView):
    def get(self, request, song_id):
        print(f"here it is {song_id}")
        # get the song from the database
        song = get_object_or_404(Song, id=song_id)
        # get the lyrics of the song
        lyrics = song.lyrics
        # call the recommend function
        recommended_songs = recommend(lyrics)
        # serializer needs to be done
        x = []
        for sid in recommended_songs:
            s = Song.objects.get(sid == id)
            x.append(s)
        serializer = SongSerializer(x, many = True)

        return Response(serializer.data)
        
