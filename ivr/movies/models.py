from django.db import models


class Theater(models.Model):
    class Meta:
        verbose_name = 'Theater'
        verbose_name_plural = 'Theaters'

    name = models.CharField(
        max_length=50,
    )
    address = models.TextField()
    digits = models.PositiveSmallIntegerField(
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    title = models.CharField(
        max_length=50,
    )
    digits = models.PositiveSmallIntegerField(
        unique=True,
    )

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
