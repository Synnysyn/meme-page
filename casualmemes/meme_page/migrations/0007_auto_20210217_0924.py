# Generated by Django 3.1.4 on 2021-02-17 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meme_page", "0006_auto_20210215_1648"),
    ]

    operations = [
        migrations.RenameField(
            model_name="genre",
            old_name="title",
            new_name="name",
        ),
        migrations.RemoveField(
            model_name="genre",
            name="memes",
        ),
        migrations.AddField(
            model_name="meme",
            name="genres",
            field=models.ManyToManyField(default=None, to="meme_page.Genre"),
        ),
    ]
