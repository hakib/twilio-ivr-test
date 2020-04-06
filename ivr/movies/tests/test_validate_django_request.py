import pytest

from unittest import mock
from django.core.exceptions import SuspiciousOperation
from django.test import RequestFactory


from ..views import validate_django_request


def test_should_not_validate_request_without_a_signature(rf: RequestFactory) -> None:
    request = rf.post('/')
    with pytest.raises(SuspiciousOperation):
        validate_django_request(request)


def test_should_not_validate_request_with_invalid_signature(rf: RequestFactory) -> None:
    request = rf.post('/', {}, HTTP_X_TWILIO_SIGNATURE='signature')
    with pytest.raises(SuspiciousOperation):
        validate_django_request(request)


def test_should_validate_request_with_a_valid_signature(rf: RequestFactory) -> None:
    request = rf.post('/', {}, HTTP_X_TWILIO_SIGNATURE='signature')
    with mock.patch('movies.views.request_validator', autospec=True) as mock_request_validator:
        mock_request_validator.validate.return_value = True
        validate_django_request(request)
