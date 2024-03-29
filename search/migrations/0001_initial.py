# Generated by Django 4.1.6 on 2023-03-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Search",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("search_query", models.CharField(max_length=100)),
                ("search_type", models.CharField(max_length=10)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
