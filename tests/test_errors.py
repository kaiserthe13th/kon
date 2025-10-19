import kon
import pytest


def test_just_comma():
    with pytest.raises(ValueError):
        kon.loads(',')


def test_just_comma_in_array():
    with pytest.raises(ValueError):
        kon.loads('[,]')


def test_just_comma_in_dict():
    with pytest.raises(ValueError):
        kon.loads('{,}')

def test_invalid_type_dumped():
    class Test:
        pass

    with pytest.raises(TypeError):
        kon.dumps(Test()) # type: ignore


def test_unterminated_str():
    with pytest.raises(ValueError):
        kon.loads('"')

def test_unterminated_esc_seq():
    with pytest.raises(ValueError):
        kon.loads('"\\')

def test_invalid_esc_seq():
    with pytest.raises(ValueError):
        kon.loads('"\\xG')
    with pytest.raises(ValueError):
        kon.loads('"\\xGE"')
    with pytest.raises(ValueError):
        kon.loads('"\\uGE"')
    with pytest.raises(ValueError):
        kon.loads('"\\uHAUI"')
