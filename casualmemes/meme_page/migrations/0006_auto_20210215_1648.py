# Generated by Django 3.1.4 on 2021-02-15 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meme_page", "0005_auto_20210215_1556"),
    ]

    operations = [
        migrations.AlterField(
            model_name="meme",
            name="image",
            field=models.ImageField(upload_to="uploads/"),
        ),
    ]
