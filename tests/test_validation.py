# test_validation.py
import pytest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from validation import Validation


@pytest.fixture
def validate():
    '''Returns a Validation instance'''
    return Validation()

@pytest.mark.parametrize("email,emailresult", [
    ("ABC123", True),
    ("123", False)
])
def test_email(validate, email,emailresult):
    assert validate.pnrvalidate(email) == emailresult

@pytest.mark.parametrize("mobile,mobileresult", [
    ("123456" ,False),
    ("1234567890",True)
])
def test_mobile(validate,mobile,mobileresult):
    assert validate.mobilevalidate(mobile) == mobileresult