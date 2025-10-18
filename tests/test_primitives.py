import kon


def test_integers():
    assert kon.loads('123') == 123
    assert kon.loads('-5') == -5


def test_floats():
    assert kon.loads('3.14') == 3.14
    assert kon.loads('-0.5') == -0.5
    assert kon.loads('1e3') == 1000.0


def test_booleans_and_null():
    assert kon.loads('true') is True
    assert kon.loads('false') is False
    assert kon.loads('null') is None


def test_dump_primitives():
    assert kon.dumps(123) == '123'
    assert kon.dumps(3.14) == '3.14'
    assert kon.dumps(True) == 'true'
    assert kon.dumps(None) == 'null'
