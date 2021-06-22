# test_validation.py
import pytest

from validation import Validation


@pytest.fixture
def validate():
    '''Returns a Validation instance'''
    return Validation()

@pytest.mark.parametrize("email,emailresult,mobile,mobileresult", [
    ("ABC123", True ,"123456" ,False),
    ("123", False ,"1234567890",True)
])

def test_email(validate, email,emailresult,mobile,mobileresult):
    assert validate.pnrvalidate(email) == emailresult

def test_mobile(validate, email,emailresult,mobile,mobileresult):
    assert validate.mobilevalidate(mobile) == mobileresult