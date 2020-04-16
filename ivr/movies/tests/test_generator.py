from typing import Dict, Generator, Union
from unittest import mock
from xml.etree import ElementTree
import pytest

from django.urls import reverse
from django.http import HttpResponse
from django.test import Client

from ..models import Theater, Movie


TwilioPhoneCall = Generator[Union[str, None], Union[str, None], None]


def initiate_twilio_phone_call(
    start_url: str,
    call_sid: str,
    from_number: str,
    client: Client,
) -> TwilioPhoneCall:
    next_url = start_url
    next_payload: Dict[str, str] = {}

    while True:
        with mock.patch('movies.views.request_validator', autospec=True) as request_validator_mock:
            request_validator_mock.validate.return_value = True
            response = client.post(next_url, {
                'CallSid': call_sid,
                'From': from_number,
                **next_payload,
            }, HTTP_X_TWILIO_SIGNATURE='signature')
        if not 200 <= response.status_code < 300:
            digits = yield 'An internal error occurred.'
            break

        tree = ElementTree.fromstring(response.content.decode())
        for element in tree:
            if element.tag == 'Say':
                assert element.text is not None, 'Say verb is empty!'
                digits = yield element.text

            elif element.tag == 'Gather':
                digits = None
                for nested_element in element:
                    if nested_element.tag == 'Say':
                        assert nested_element.text is not None, 'Say verb is empty!'
                        digits = yield nested_element.text
                        if digits is not None:
                            break

                    else:
                        assert f'Unimplemented verb inside Gather: {nested_element.tag}'
                if digits is not None:
                    next_url = element.get('action', next_url)
                    next_payload = {'Digits': digits}
                    break

            elif element.tag == 'Redirect':
                assert element.text is not None, 'Redirect tag is empty!'
                next_url = element.text
                break

            elif element.tag == 'Hangup':
                # Indicate end of call.
                yield None
                return

            else:
                assert f'Unimplemented verb: {element.tag}'


@pytest.fixture
def showtimes_phone_call(client: Client) -> TwilioPhoneCall:
    return initiate_twilio_phone_call(
        start_url = reverse('choose-theater'),
        call_sid = 'call-sid-1',
        from_number = '123456789',
        client = client,
    )


def test_should_tell_caller_there_are_no_showtimes(
    db,
    theater_A: Theater,
    theater_B: Theater,
    movie_A: Movie,
    movie_B: Movie,
    showtimes_phone_call: TwilioPhoneCall,
) -> None:
    assert showtimes_phone_call.send(None) == 'Welcome to movie info!'
    assert showtimes_phone_call.send(None) == 'Please choose a theater and press #'
    assert showtimes_phone_call.send(None) == 'For Theater A at A street press 1'
    assert showtimes_phone_call.send(None) == 'For Theater B at B street press 2'
    assert showtimes_phone_call.send(theater_A.digits) == 'Please choose a movie and press #'
    assert showtimes_phone_call.send(None) == 'For Movie A press 1'
    assert showtimes_phone_call.send(None) == 'For Movie B press 2'
    assert showtimes_phone_call.send(movie_A.digits) == 'Sorry, the movie is not playing any time soon in this theater.'
    assert showtimes_phone_call.send(None) == 'Thank you for using movie info!'
    assert showtimes_phone_call.send(None) is None
