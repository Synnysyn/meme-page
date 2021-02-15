from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.enums import Choices
from django.db.models.fields.files import ImageField


REACTIONS = (
    (1, "love"),
    (2, "surprised"),
    (3, "sad"),
    (4, "hate"),
)


class Meme(models.Model):
    title = models.CharField(max_length=64)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return f"{self.title} by {self.creator.username}"


class Reaction(models.Model):
    reaction_from = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_to = models.ForeignKey(Meme, on_delete=models.CASCADE)
    reaction = models.IntegerField(choices=REACTIONS)


class Report(models.Model):
    reported = models.ForeignKey(Meme, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"{self.reported.title} reported: {self.message}"


class Genre(models.Model):
    title = models.CharField(max_length=64)
    memes = models.ManyToManyField(Meme, default=None)

    def __str__(self):
        return f"{self.title}"
