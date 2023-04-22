import uuid
from django.db import models
from django.utils.text import slugify
from users.models import User
from common.utils.mime_validator import FileMimeValidator
from common.utils.upload_path import file_upload_path
from common.utils.unique_slugify import unique_slugify

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
    slug = models.SlugField(unique=True, blank=True)
    number_of_episodes = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        super(StudioPodcast, self).save(*args, **kwargs)

    def __str__(self):
        return '{0}\'s podcast - {1}'.format(self.author, self.title)


class StudioEpisode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index = models.IntegerField(blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    podcast = models.ForeignKey(StudioPodcast, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to=file_upload_path,
                            validators=[FileMimeValidator("AUDIO")])

    def __str__(self):
        return 'Episode {0} of {1} - {2}'.format(self.index, self.podcast.title, self.title)

    def save(self, *args, **kwargs):
        if self._state.adding:
            podcast = self.podcast
            podcast.number_of_episodes += 1
            podcast.save()
            self.index = self.podcast.number_of_episodes

        if not self.slug:
            self.slug = (self.title)
        super(StudioEpisode, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        podcast = self.podcast
        podcast.number_of_episodes -= 1
        podcast.save()

        storage, path = self.file.storage, self.file.path
        super(StudioEpisode, self).delete(*args, **kwargs)
        storage.delete(path)
