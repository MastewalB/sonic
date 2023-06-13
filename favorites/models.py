from django.db import models
from users.models import User
from playlists.models import Playlist
from music.models import Album
# Create your models here.


class LikedSongsPlaylist(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)


class LikedAlbums(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Liked Album"
        verbose_name_plural = "Liked Albums"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'album_id'], name='unique_album_favorite')
        ]
