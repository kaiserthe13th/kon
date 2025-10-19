import kon


def test_pretty_list():
    val = []
    assert kon.dumps(val, pretty=True) == '()'
    val.append(2)
    assert kon.dumps(val, pretty=True) == '(2)'
    val.append(3)
    assert kon.dumps(val, pretty=True) == '(\n  2\n  3\n)'
    val.append([1])
    assert kon.dumps(val, pretty=True) == '(\n  2\n  3\n  (1)\n)'

def test_pretty_dict():
    val = {}
    assert kon.dumps(val, pretty=True) == '{}'
    val[1] = 2
    assert kon.dumps(val, pretty=True) == '1 = 2'
    val[2] = {'abc': 'def'}
    assert kon.dumps(val, pretty=True) == '1 = 2\n2 abc = def'
    val[2]['gulp'] = 'tomb'
    assert kon.dumps(val, pretty=True) == '1 = 2\n2 {\n  abc = def\n  gulp = tomb\n}'
    val[2] = [1]
    assert kon.dumps(val, pretty=True) == '1 = 2\n2(1)'
