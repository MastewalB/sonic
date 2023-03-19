from django.db import models
from users.models import User

# Create your models here.
class Playlist(models.Model):
    playlist_id = models.BigAutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_title = models.CharField(max_length=255)

class PlaylistItems(models.Model):
    playlist_id = models.BigAutoField()
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
