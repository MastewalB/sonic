# Generated by Django 4.1.6 on 2023-04-11 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='podcast',
            name='unique_podcast',
        ),
        migrations.AlterField(
            model_name='podcastsubscription',
            name='podcast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcast.podcast', unique=True),
        ),
        migrations.AddConstraint(
            model_name='podcast',
            constraint=models.UniqueConstraint(fields=('podcast_id', 'provider'), name='unique_podcast'),
        ),
    ]
