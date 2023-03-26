from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from .models import Search
from .serializers import SearchSerializer
from music.models import Album, Artist, Song
from music.serializers import AlbumSerializer, ArtistSerializer, SongSerializer


class SearchView(generics.ListAPIView):
    serializer_class = SearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('search_query', None)
        print(query)
        if query is None:
            return Search.objects.none()

        album_query = Q(name__icontains=query)
        artist_query = Q(name__icontains=query)
        song_query = Q(title__icontains=query) | Q(
            s_artist__name__icontains=query) | Q(s_album__name__icontains=query)

        search_results = [
            {
                'type': 'album',
                'data': AlbumSerializer(album).data,
                'score': album.name.lower().count(query.lower()),
            }
            for album in Album.objects.filter(album_query)
        ] + [
            {
                'type': 'artist',
                'data': ArtistSerializer(artist).data,
                'score': artist.name.lower().count(query.lower()),
            }
            for artist in Artist.objects.filter(artist_query)
        ] + [
            {
                'type': 'song',
                'data': SongSerializer(song).data,
                'score': song.title.lower().count(query.lower()) + song.s_artist.name.lower().count(query.lower()) + song.s_album.name.lower().count(query.lower()),
            }
            for song in Song.objects.filter(song_query)
        ]

        # Sort the results by score in descending order
        search_results = sorted(
            search_results, key=lambda x: x['score'], reverse=True)

        # Save the search query to the database
        search = Search(search_query=query, search_type='all')
        search.save()
        print(search_results)

        return search_results
