from django.db import models
from users.models import User

# Create your models here.
class Playlist(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    song_item = models.ForeignKey(Song, on_delete=models.CASCADE, null=True)

    playlist_title = models.CharField(max_length=255)
