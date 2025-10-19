import math
import pytest
import kon


def test_integers():
    assert kon.loads("123") == 123
    assert kon.loads("-5") == -5
    assert kon.loads("0x1ca67b") == 0x1ca67b
    assert kon.loads("0o1337") == 0o1337
    assert kon.loads("0b1001") == 0b1001

def test_multiple_negation():
    assert kon.loads('---132') == -132
    assert kon.loads('-+-42') == 42


def test_negation_error_type():
    with pytest.raises(TypeError):
        kon.loads("-'a'")
    with pytest.raises(TypeError):
        kon.loads("+()")

def test_floats():
    assert kon.loads("3.14") == 3.14
    assert kon.loads("-0.5") == -0.5
    assert kon.loads("1e3") == 1000.0
    assert kon.loads("inf") == float('inf')
    assert math.isinf(kon.loads("inf")) # type: ignore
    assert math.isnan(kon.loads("nan")) # type: ignore


def test_booleans_and_null():
    assert kon.loads("true") is True
    assert kon.loads("false") is False
    assert kon.loads("null") is None


def test_dump_primitives():
    assert kon.dumps(123) == "123"
    assert kon.dumps(3.14) == "3.14"
    assert kon.dumps(True) == "true"
    assert kon.dumps(None) == "null"


def test_huge_exponents_neg():
    assert kon.loads("123.456e-789") == 123.456e-789


def test_huge_exponents_pos():
    assert (
        kon.loads(
            "0.4e00669999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999969999999006"
        )
        == 0.4e00669999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999969999999006
    )
