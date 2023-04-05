from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from .models import Search
from .serializers import SearchSerializer
from music.models import Album, Artist, Song
from music.serializers import AlbumSerializer, ArtistSerializer, SongSerializer
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from django.db.models import Q, Value, TextField, CharField
from django.db.models.functions import Concat
from django.contrib.postgres.search import SearchRank
from django.contrib.postgres.search import TrigramSimilarity

from itertools import islice, chain


class QuerySetChain(object):
    """
    Chains multiple subquerysets (possibly of different models) and behaves as
    one queryset.  Supports minimal methods needed for use with
    django.core.paginator.
    """

    def __init__(self, *subquerysets):
        self.querysets = subquerysets

    def count(self):
        """
        Performs a .count() for all subquerysets and returns the number of
        records as an integer.
        """
        return sum(qs.count() for qs in self.querysets)

    def _clone(self):
        "Returns a clone of this queryset chain"
        return self.__class__(*self.querysets)

    def _all(self):
        "Iterates records in all subquerysets"
        return chain(*self.querysets)

    def __getitem__(self, ndx):
        """
        Retrieves an item or slice from the chained set of results from all
        subquerysets.
        """
        if type(ndx) is slice:
            return list(islice(self._all(), ndx.start, ndx.stop, ndx.step or 1))
        else:
            return islice(self._all(), ndx, ndx+1).next()


class SearchView(generics.ListAPIView):
    serializer_class = SearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('search_query', None)
        print(query)
        if query is None:
            return Search.objects.none()
        # ******************************************************
        album_query = Q(name__icontains=query)
        artist_query = Q(name__icontains=query)
        song_query = Q(title__icontains=query) | Q(
            s_artist__name__icontains=query) | Q(s_album__name__icontains=query)

        album_results = Album.objects.filter(album_query)
        artist_results = Artist.objects.filter(artist_query)
        song_results = Song.objects.filter(song_query)

        search_results = []
        for album in album_results:
            search_results.append({
                'type': 'album',
                'data': album
            })

        for artist in artist_results:
            search_results.append({
                'type': 'artist',
                'data': artist
            })

        for song in song_results:
            search_results.append({
                'type': 'song',
                'data': song
            })

        return search_results
        # *********************************************************
        album_query = Q(name__icontains=query)
        artist_query = Q(name__icontains=query)
        song_query = Q(title__icontains=query) | Q(
            s_artist__name__icontains=query) | Q(s_album__name__icontains=query)

        # search_results = [
        #     {
        #         'type': 'album',
        #         'data': AlbumSerializer(album).data,
        #         'score': album.name.lower().count(query.lower()),
        #     }
        #     for album in Album.objects.filter(album_query)
        # ] + [
        #     {
        #         'type': 'artist',
        #         'data': ArtistSerializer(artist).data,
        #         'score': artist.name.lower().count(query.lower()),
        #     }
        #     for artist in Artist.objects.filter(artist_query)
        # ] + [
        #     {
        #         'type': 'song',
        #         'data': SongSerializer(song).data,
        #         'score': song.title.lower().count(query.lower()) + song.s_artist.name.lower().count(query.lower()) + song.s_album.name.lower().count(query.lower()),
        #     }
        #     for song in Song.objects.filter(song_query)
        # ]

        # # Sort the results by score in descending order
        # search_results = sorted(
        #     search_results, key=lambda x: x['score'], reverse=True)

        # return search_results

        # Save the search query to the database
        # search = Search(search_query=query, search_type='all')
        # search.save()
        # print(search_results)
        # serialized_search_results = SearchSerializer(search_results, many=True)

        # data = [{'id': 0, 'name': 'search'}
        #         for obj in search_results]  # Convert queryset to a list of dicts
        # return JsonResponse(data, safe=False)
        # return serialized_search_results.data

        albums = Album.objects.filter(album_query)

        artists = Artist.objects.filter(artist_query)

        songs = Song.objects.filter(song_query)

        renderer = JSONRenderer()
        renderer_context = {'indent': 4}

        return QuerySetChain(albums, artists, songs)
        return Response(renderer.render({
            "albums":  AlbumSerializer(instance=albums, many=True).data,
            "artists": ArtistSerializer(instance=artists, many=True).data,
            "songs": SongSerializer(instance=songs, many=True).data,
        }))

        return JsonResponse(search_results, safe=False)
