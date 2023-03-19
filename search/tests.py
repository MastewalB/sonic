from django.test import TestCase

# Create your tests here.
#this is an alternative to try searching by calculating a score
#on appearance of each keyword

from django.db import models
from django.db.models import Count

class Album(models.Model):
    title = models.CharField(max_length=255)

class Artist(models.Model):
    name = models.CharField(max_length=255)

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

class SearchResult(models.Model):
    title = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    object_id = models.PositiveIntegerField()
    score = models.FloatField(default=0)

    @classmethod
    def search(cls, query):
        results = []
        # calculate keyword frequency for the query
        keyword_frequency = {}
        for keyword in query.split():
            keyword_frequency[keyword] = keyword_frequency.get(keyword, 0) + 1
        # search for albums, artists, and songs that match the query
        for album in Album.objects.annotate(score=Count('title', filter=models.Q(title__icontains=query))).filter(score__gt=0):
            result = SearchResult(title=album.title, model_name='album', object_id=album.id)
            # calculate score for the album based on keyword frequency
            for keyword, frequency in keyword_frequency.items():
                if keyword in result.title.lower():
                    result.score += frequency
            results.append(result)
        for artist in Artist.objects.annotate(score=Count('name', filter=models.Q(name__icontains=query))).filter(score__gt=0):
            result = SearchResult(title=artist.name, model_name='artist', object_id=artist.id)
            # calculate score for the artist based on keyword frequency
            for keyword, frequency in keyword_frequency.items():
                if keyword in result.title.lower():
                    result.score += frequency
            results.append(result)
        for song in Song.objects.annotate(score=Count('title', filter=models.Q(title__icontains=query))).filter(score__gt=0):
            result = SearchResult(title=song.title, model_name='song', object_id=song.id)
            # calculate score for the song based on keyword frequency
            for keyword, frequency in keyword_frequency.items():
                if keyword in result.title.lower() or keyword in song.artist.name.lower() or keyword in song.album.title.lower():
                    result.score += frequency
            results.append(result)
        # sort the results by score in descending order
        results.sort(key=lambda x: x.score, reverse=True)
        return results
