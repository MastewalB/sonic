import uuid
from django.db import models
from users.models import User
from common.utils.mime_validator import FileMimeValidator
from common.utils.upload_path import file_upload_path

# Create your models here.


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class StudioPodcast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    genre = models.TextField()
    number_of_episodes = models.IntegerField(default=0)

    def __str__(self):
        return '{0}\'s podcast - {1}'.format(self.author, self.title)


class StudioEpisode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    podcast = models.ForeignKey(StudioPodcast, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to=file_upload_path,
                            validators=[FileMimeValidator("AUDIO")])

    def __str__(self):
        return '{0} Episode - {1}'.format(self.podcast.title, self.title)

    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super(StudioEpisode, self).delete(*args, **kwargs)
        storage.delete(path)
