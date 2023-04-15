from django.db import models
from common.utils.mime_validator import FileMimeValidator
from common.utils.upload_path import file_upload_path

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=55)
    picture = models.URLField(blank=True)


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False, null=False)
    cover = models.URLField(blank=True)


class Song(models.Model):
    title = models.CharField(max_length=35)
    s_artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    s_album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_file = models.FileField(upload_to=file_upload_path, validators=[
                                 FileMimeValidator("AUDIO")])
    content_type = models.CharField(max_length=50)
