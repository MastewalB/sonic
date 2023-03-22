from django.db import models
from users.models import User
from music.models import Song
import uuid

# Create your models here.
class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_title = models.CharField(max_length=255)

class PlaylistItems(models.Model):
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    class Meta:
        db_table = 'playlist-items'
        constraints = [
            models.UniqueConstraint(fields=['playlist_id', 'song_id'], name='unique playlist-items')
        ]