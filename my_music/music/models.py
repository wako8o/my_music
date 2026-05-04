from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from my_music.music.choices import GenreChoices
from my_music.music.validatiors import validators_username


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    MAX_LENGTH_NAME = 15
    MIN_LENGTH_NAME = 2
    username = models.CharField(
        max_length=MAX_LENGTH_NAME,
        validators=[
            validators_username,
            MinLengthValidator(MIN_LENGTH_NAME),
        ],

        null=False,
        blank=False,

    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.username

class Album(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='albums',
    )

    MAX_LENGTH_ALBUM_NAME = 30
    MAX_LENGTH_NAME_GENRE = 30
    MAX_LENGTH_NAME_ARTIST = 30

    album_name = models.CharField(
        verbose_name = 'Nombre de album',
        max_length=MAX_LENGTH_ALBUM_NAME,
        unique=True,
        null=False,
        blank=False,
    )

    artist = models.CharField(
        max_length=MAX_LENGTH_NAME_ARTIST,
        null=False,
        blank=False,
    )

    genre = models.CharField(
        verbose_name = 'Genere',
        max_length=MAX_LENGTH_NAME_GENRE,
        choices=GenreChoices,
        null=False,
        blank=False,
    )

    descriptions = models.TextField(
        verbose_name = 'Descripciones',
        null=True,
        blank=True,
    )

    image_url = models.URLField(
        verbose_name= 'Imagen URL',
        unique=True,
        null=False,
        blank=False,
    )

    price = models.FloatField(
        verbose_name = 'Precio',
        validators=[
            MinValueValidator(0.0, message='Цената не може да е по-ниска от 0.0'),
        ],
        null=False,
        blank=False
    )

    class Meta:
        ordering = ['pk']
