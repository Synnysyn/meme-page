from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.enums import Choices
from django.db.models.fields.files import ImageField
from django.forms import widgets


REACTIONS = (
    (1, "😍"),
    (2, "😲"),
    (3, "😥"),
    (4, "😡"),
)


class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Meme(models.Model):
    title = models.CharField(max_length=64)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/")
    genres = models.ManyToManyField(Genre, default=None)

    def __str__(self):
        return f"{self.title} by {self.creator.username}"


class Reaction(models.Model):
    reaction_from = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_to = models.ForeignKey(Meme, on_delete=models.CASCADE)
    reaction = models.IntegerField(choices=REACTIONS)

    def __str__(self):
        return f"{REACTIONS[self.reaction - 1][1]} {self.reaction_from} -> {self.reaction_to}"


class Report(models.Model):
    reported = models.ForeignKey(Meme, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"{self.reported.title} reported: {self.message}"


class Avatar(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/avatars/")
