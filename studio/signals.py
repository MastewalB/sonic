from django.db.models.signals import post_save
from django.dispatch import receiver
from studio.models import StudioPodcast, StudioEpisode


@receiver(post_save, sender=StudioEpisode, dispatch_uid='update_episode_count')
def increment_episode_count(sender, instance, created, **kwargs):
    print("Hereeeeeeeeeeeeeeeeeee")
    if created:
        instance.podcast.number_of_episodes += 1
        instance.podcast.save()

    # if created:
    #     try:
    #         podcast = StudioPodcast.objects.get(id=instance.podcast.id)
    #         podcast.number_of_episodes += 1
    #         podcast.save()
    #     except StudioPodcast.DoesNotExist:
    #         raise ValueError("No Such Podcast")
