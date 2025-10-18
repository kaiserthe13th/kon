import pytest
import kon


def test_empty_dict():
    assert kon.loads("{}") == {}


def test_simple_dict():
    assert kon.loads("{a = 1, b = 2}") == {"a": 1, "b": 2}


def test_nested_dict():
    assert kon.loads("{a = {b = {c = 3}}}") == {"a": {"b": {"c": 3}}}


def test_nested_dict_shorthand():
    assert kon.loads("a b c = 3") == {"a": {"b": {"c": 3}}}


def test_nested_dict_shorthand_list_syntax():
    assert kon.loads("a b c(3, d, e)") == {"a": {"b": {"c": [3, "d", "e"]}}}

def test_nested_dict_shorthand_dict_syntax():
    assert kon.loads("a b c {3 = d, 3.14 = e}") == {"a": {"b": {"c": {3: "d", 3.14:"e"}}}}


def test_unset_key_in_implicit_dict():
    with pytest.raises(ValueError):
        kon.loads("a b c")


def test_unset_key_in_dict():
    with pytest.raises(ValueError):
        kon.loads("a b { c }")

def test_numeric_and_mixed_keys():
    # numeric keys supported in dumps; when parsing, numeric-looking keys become numbers
    assert kon.loads('{1 = "one", 2.0 = 2}') == {1: "one", 2.0: 2}


def test_mixed_values():
    assert kon.loads('{a = (1, 2), b = null, c = true, d = "str \\nwith\\r\\nsome lines\\t"}') == {
        "a": [1, 2],
        "b": None,
        "c": True,
        "d": "str \nwith\r\nsome lines\t",
    }
