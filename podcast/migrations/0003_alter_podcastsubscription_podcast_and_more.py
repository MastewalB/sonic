# Generated by Django 4.1.6 on 2023-04-17 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0002_remove_podcast_unique_podcast_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='podcastsubscription',
            name='podcast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcast.podcast'),
        ),
        migrations.AddConstraint(
            model_name='podcastsubscription',
            constraint=models.UniqueConstraint(fields=('user', 'podcast'), name='unique_subscription'),
        ),
    ]
