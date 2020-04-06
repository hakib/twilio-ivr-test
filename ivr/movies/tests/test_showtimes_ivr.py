import pytest
import datetime
import pytz
from unittest import mock
from django.urls import reverse
from django.test import Client

from ..models import Theater, Movie, Show
from .twilio_phone_call import TwilioPhoneCall


@pytest.fixture
def showtimes_phone_call(client: Client) -> TwilioPhoneCall:
    return TwilioPhoneCall(
        start_url = reverse('choose-theater'),
        client = client,
        call_sid = 'call-sid-1',
        from_number = '123456789',
    )


def test_should_tell_caller_there_are_no_showtimes(
    db,
    showtimes_phone_call: TwilioPhoneCall,
    theater_A: Theater,
    theater_B: Theater,
    movie_A: Movie,
    movie_B: Movie,
) -> None:
    response = showtimes_phone_call.initiate()
    content = response.content.decode()
    assert '<Say>Welcome to movie info!</Say>' in content
    assert '<Say>For Theater A at A street press 1</Say>' in content
    assert '<Say>For Theater B at B street press 2</Say>' in content

    response = showtimes_phone_call.enter_digits(theater_A.digits)
    content = response.content.decode()
    assert '<Say>Please choose a movie and press #</Say>' in content
    assert '<Say>For Movie A press 1</Say>' in content
    assert '<Say>For Movie B press 2</Say>' in content

    response = showtimes_phone_call.enter_digits(movie_A.digits)
    content = response.content.decode()
    assert '<Say>Sorry, the movie is not playing any time soon in this theater.</Say>' in content
    assert showtimes_phone_call.call_ended


def test_should_list_showtimes(
    db,
    showtimes_phone_call: TwilioPhoneCall,
    theater_A: Theater,
    movie_A: Movie,
) -> None:
    showtimes_phone_call.initiate()
    showtimes_phone_call.enter_digits(theater_A.digits)

    now = datetime.datetime(2020, 5, 1, 13, 30, tzinfo=pytz.UTC)
    Show.objects.create(movie=movie_A, theater=theater_A, starts_at=now)
    with mock.patch('movies.views.timezone') as mock_timezone:
        mock_timezone.now.return_value = now
        response = showtimes_phone_call.enter_digits(movie_A.digits)
        content = response.content.decode()
        assert '<Say>The movie Movie A will be playing at Theater A at 01:30PM</Say>' in content

    assert showtimes_phone_call.call_ended


def test_should_repeat_theater_selection_when_caller_did_not_press_any_key(
    db,
    showtimes_phone_call: TwilioPhoneCall,
    theater_A: Theater,
) -> None:
    response = showtimes_phone_call.initiate()
    assert '<Say>Welcome to movie info!</Say>' in response.content.decode()

    response = showtimes_phone_call.timeout()
    assert '<Say>Welcome to movie info!</Say>' in response.content.decode()


def test_should_repeat_theater_selection_when_caller_selected_non_existing_theater(
    db,
    showtimes_phone_call: TwilioPhoneCall,
    theater_A: Theater,
) -> None:
    response = showtimes_phone_call.initiate()
    assert '<Say>Welcome to movie info!</Say>' in response.content.decode()

    response = showtimes_phone_call.enter_digits('10')
    assert '<Say>Welcome to movie info!</Say>' in response.content.decode()


def test_should_repeat_movie_selection_when_caller_did_not_press_any_key(
    db,
    showtimes_phone_call: TwilioPhoneCall,
    theater_A: Theater,
    movie_A: Movie,
) -> None:
    showtimes_phone_call.initiate()
    response = showtimes_phone_call.enter_digits(theater_A.digits)
    assert '<Say>Please choose a movie and press #</Say>' in response.content.decode()

    showtimes_phone_call.timeout()
    assert '<Say>Please choose a movie and press #</Say>' in response.content.decode()


def test_should_repeat_movie_selection_when_caller_selected_non_existing_movie(
    db,
    showtimes_phone_call: TwilioPhoneCall,
    theater_A: Theater,
    movie_A: Movie,
) -> None:
    showtimes_phone_call.initiate()
    response = showtimes_phone_call.enter_digits(theater_A.digits)
    assert '<Say>Please choose a movie and press #</Say>' in response.content.decode()

    showtimes_phone_call.enter_digits('10')
    assert '<Say>Please choose a movie and press #</Say>' in response.content.decode()


def test_should_list_multiple_showtimes(
    db,
    showtimes_phone_call: TwilioPhoneCall,
    theater_A: Theater,
    movie_A: Movie,
) -> None:
    now = datetime.datetime(2020, 5, 1, 13, 30, tzinfo=pytz.UTC)
    Show.objects.create(movie=movie_A, theater=theater_A, starts_at=now)
    Show.objects.create(movie=movie_A, theater=theater_A, starts_at=now + datetime.timedelta(minutes=30))

    showtimes_phone_call.initiate()
    showtimes_phone_call.enter_digits(theater_A.digits)
    with mock.patch('movies.views.timezone') as mock_timezone:
        mock_timezone.now.return_value = now
        response = showtimes_phone_call.enter_digits(movie_A.digits)
        assert '<Say>The movie Movie A will be playing at Theater A at 01:30PM, 02:00PM</Say>' in response.content.decode()


def test_should_only_list_shows_that_are_playing_soon(
    db,
    showtimes_phone_call: TwilioPhoneCall,
    theater_A: Theater,
    movie_A: Movie,
) -> None:
    now = datetime.datetime(2020, 5, 1, 13, 30, tzinfo=pytz.UTC)
    # Show that already started
    Show.objects.create(movie=movie_A, theater=theater_A, starts_at=now - datetime.timedelta(minutes=30))
    # Show in more than 12 hours
    Show.objects.create(movie=movie_A, theater=theater_A, starts_at=now + datetime.timedelta(hours=12, minutes=1))

    showtimes_phone_call.initiate()
    showtimes_phone_call.enter_digits(theater_A.digits)
    with mock.patch('movies.views.timezone') as mock_timezone:
        mock_timezone.now.return_value = now
        response = showtimes_phone_call.enter_digits(movie_A.digits)
        assert '<Say>Sorry, the movie is not playing any time soon in this theater.</Say>' in response.content.decode()
