import datetime

from django.utils import timezone

from movies.models import Theater, Movie, Show

now = timezone.now()
HOUR = datetime.timedelta(hours=1)


castro_theatre = Theater.objects.create(
    name='Castro Theatre',
    address='San Francisco, California',
    digits=1,
)
alamo_drafthouse = Theater.objects.create(
    name='Alamo Drafthouse',
    address='Austin, Texas',
    digits=2,
)

clockwork_orange = Movie.objects.create(
    title='Clockwork Orange',
    digits=1,
)
godfather = Movie.objects.create(
    title='The Godfather',
    digits=2,
)

Show.objects.bulk_create([
    Show(theater=castro_theatre,  movie=clockwork_orange, starts_at=now + 1 * HOUR),
    Show(theater=castro_theatre,  movie=clockwork_orange, starts_at=now + 2 * HOUR),
    Show(theater=castro_theatre,  movie=godfather,        starts_at=now + 3 * HOUR),
    Show(theater=castro_theatre,  movie=godfather,        starts_at=now + 6 * HOUR),
    Show(theater=castro_theatre,  movie=godfather,        starts_at=now + 9 * HOUR),

    Show(theater=alamo_drafthouse, movie=clockwork_orange, starts_at=now),
    Show(theater=alamo_drafthouse, movie=clockwork_orange, starts_at=now + 4 * HOUR),
    Show(theater=alamo_drafthouse, movie=clockwork_orange, starts_at=now + 8 * HOUR),
    Show(theater=alamo_drafthouse, movie=godfather,        starts_at=now + 1 * HOUR),
    Show(theater=alamo_drafthouse, movie=godfather,        starts_at=now + 6 * HOUR),
])
