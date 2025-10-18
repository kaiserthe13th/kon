import textwrap
import pytest
import kon


def test_empty_list():
    assert kon.loads("()") == []


def test_simple_list():
    assert kon.loads("(1, 2, 3)") == [1, 2, 3]


def test_nested_lists():
    assert kon.loads("((1, 2), (3, 4))") == [[1, 2], [3, 4]]


def test_list_with_identifiers_and_booleans():
    # identifiers parsed as strings; null/true/false handled by identifier parser
    assert kon.loads("(hello, true, false, null)") == ["hello", True, False, None]


def test_list_with_mixed_types():
    assert kon.loads('(1, "two", (3, 4), {a = 5})') == [1, "two", [3, 4], {"a": 5}]


def test_list_using_newline_as_comma():
    # identifiers parsed as strings; null/true/false handled by identifier parser
    assert kon.loads(
        textwrap.dedent("""
        (
            hello
            true
            false
            null
        )
""")
    ) == ["hello", True, False, None]
