from django.db import models
from common.utils.mime_validator import FileMimeValidator
from common.utils.upload_path import file_upload_path

import uuid
# Create your models here.


class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=55)
    picture = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False, null=False)
    cover = models.URLField(blank=True)

    def __str__(self):
        return "{0} by {1}".format(self.name, self.artist)


class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=35)
    s_artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    s_album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_file = models.FileField(upload_to=file_upload_path, validators=[
                                 FileMimeValidator("AUDIO")])
    content_type = models.CharField(max_length=50)
    lyrics = models.TextField(blank=True, null=True)

    def delete(self, *args, **kwargs):
        storage, path = self.song_file.storage, self.song_file.path
        super(Song, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return "{0} by {1}".format(self.title, self.s_artist)
