"""
test handle_result
    - success -> should return the result
    - fail -> raise exception
"""
from pytest import raises
from app.utils.service_result import handle_result, ServiceResult
from app.exceptions.base import AppExceptionCase


def test_handle_result_success():

    sr = ServiceResult(1)
    assert handle_result(sr) == 1


def test_handle_result_failure():

    sr = ServiceResult(AppExceptionCase(500, context=None))
    with raises(AppExceptionCase):
        handle_result(sr)
