from django.db import models


class Theater(models.Model):

    class Meta:
        verbose_name = 'Theater'
        verbose_name_plural = 'Theaters'

    name = models.CharField(max_length=50)
    address = models.TextField()
    digits = models.PositiveSmallIntegerField(unique=True)

    def __str__(self) -> str:
        return self.name

"""
from movies.models import Theater

castro_theatre = Theater.objects.create(name='Castro Theatre', address='San Francisco, California', digits=1)
alamo_drafthouse = Theater.objects.create(name='Alamo Drafthouse', address='Austin, Texas', digits=2)

from movies.models import Movie

clockwork_orange = Movie.objects.create(title='Clockwork Orange', digits=1)
godfather = Movie.objects.create(title='The Godfather', digits=2)

import datetime
from movies.models import Show
from django.utils import timezone

now = timezone.now()
hour = datetime.timedelta(hours=1)

Show.objects.bulk_create([
    Show(theater=castro_theatre,  movie=clockwork_orange, starts_at=now + hour),
    Show(theater=castro_theatre,  movie=clockwork_orange, starts_at=now + 2.5 * hour),
    Show(theater=castro_theatre,  movie=godfather,        starts_at=now + 3 * hour),
    Show(theater=castro_theatre,  movie=godfather,        starts_at=now + 6 * hour),
    Show(theater=castro_theatre,  movie=godfather,        starts_at=now + 9 * hour),

    Show(theater=alamo_drafthouse, movie=clockwork_orange, starts_at=now),
    Show(theater=alamo_drafthouse, movie=clockwork_orange, starts_at=now + hour * 4),
    Show(theater=alamo_drafthouse, movie=clockwork_orange, starts_at=now + hour * 8),
    Show(theater=alamo_drafthouse, movie=godfather,        starts_at=now + hour),
    Show(theater=alamo_drafthouse, movie=godfather,        starts_at=now + 6 * hour),
])
"""

class Movie(models.Model):

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    title = models.CharField(max_length=50)
    digits = models.PositiveSmallIntegerField(unique=True)

    def __str__(self) -> str:
        return self.title


class Show(models.Model):

    class Meta:
        verbose_name = 'Show'
        verbose_name_plural = 'Shows'

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
    )

    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE,
    )

    starts_at = models.DateTimeField()
