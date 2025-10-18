import textwrap
import pytest
import kon


def test_simple_string():
    s = '"hello"'
    assert kon.loads(s) == "hello"


def test_escaped_chars():
    s = '"line\\nsecond\\tend"'
    assert kon.loads(s) == "line\nsecond\tend"


def test_dedent_multiline_with_marker():
    example = "\n    a\n      b\n"
    src = f'<"{example}"'
    # using marker < should dedent
    if example.startswith('\n'):
        example = example[1:]
    example = textwrap.dedent(example)

    assert kon.loads(src) == example


def test_ignore_multiline_with_marker():
    example = "\n    a\n      b\n"
    src = f'|"{example}"'
    # | should preserve indentation (but still remove leading newline handling is up to parser)
    assert kon.loads(src) == example


def test_value_error_on_multiline_default():
    # parser configured with VALUE_ERROR should reject multiline when no marker preference passed
    with pytest.raises(ValueError):
        kon.loads('"\nline\n"', multiline_string_behaviour=kon.MultilineStringBehaviour.VALUE_ERROR)
