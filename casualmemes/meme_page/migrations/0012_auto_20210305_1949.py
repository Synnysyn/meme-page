# Generated by Django 3.1.4 on 2021-03-05 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meme_page', '0011_meme_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meme',
            name='genres',
            field=models.ManyToManyField(blank=True, default=None, to='meme_page.Genre'),
        ),
    ]
