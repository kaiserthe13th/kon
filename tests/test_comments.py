import kon


def test_comments_simple():
    assert kon.loads('true # false') is True


def test_commented_dict():
    assert kon.loads('a # {  }') == 'a'
