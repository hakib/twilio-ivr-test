import pytest

from ..models import Theater, Movie


@pytest.fixture
def theater_A(db) -> Theater:
    return Theater.objects.create(
        name='Theater A',
        address='A street',
        digits=1,
    )


@pytest.fixture
def theater_B(db) -> Theater:
    return Theater.objects.create(
        name='Theater B',
        address='B street',
        digits=2,
    )


@pytest.fixture
def movie_A(db) -> Movie:
    return Movie.objects.create(
        title='Movie A',
        digits=1,
    )


@pytest.fixture
def movie_B(db) -> Movie:
    return Movie.objects.create(
        title='Movie B',
        digits=2,
    )
