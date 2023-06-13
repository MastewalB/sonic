from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import User
from playlists.models import Playlist
from favorites.models import LikedSongsPlaylist
from gstream.models import Stream


@receiver(post_save, sender=User)
def create_playlist(sender, instance, created, **kwargs):
    if created:
        liked_songs_playlist = None
        try:
            liked_songs_playlist = Playlist(
                created_by=instance.id, playlist_title="Liked Songs")
            liked_songs_playlist.save()

        except (Playlist.DoesNotExist, Exception) as e:
            liked_songs_playlist = None

        if liked_songs_playlist is not None:
            try:
                liked_songs_store = LikedSongsPlaylist(
                    user_id=instance.id, playlist_id=liked_songs_playlist.id)
                liked_songs_store.save()
            except (LikedSongsPlaylist.DoesNotExist, Exception) as e:
                liked_songs_store = None
    else:
        try:
            playlist = LikedSongsPlaylist.objects.get(user_id=instance.id)

        except (LikedSongsPlaylist.DoesNotExist, Exception) as e:

            playlist, created = Playlist.objects.get_or_create(
                created_by=instance.id, playlist_title="Liked Songs")
            liked_songs_store = LikedSongsPlaylist(
                user_id=instance.id, playlist_id=playlist.id)


@receiver(post_save, sender=User)
def create_stream_table(sender, instance, created, **kwargs):
    if created:
        stream_table = None
        try:
            stream_table = Stream(user_id=instance.id)
            stream_table.save()
        except Exception as e:
            stream_table = None
    else:
        try:
            stream_table = Stream.objects.get(user_id=instance.id)
        except (Stream.DoesNotExist, Exception) as e:
            stream_table, created = Stream.objects.get_or_create(
                user_id=instance.id)


post_save.connect(create_playlist, sender=User)
post_save.connect(create_stream_table, sender=User)
