import kon
import pytest


def test_dump_then_load():
    v1_dict = {'a': 4}
    assert kon.loads(kon.dumps(v1_dict)) == v1_dict
    v2_list = ['cute', 'little', 'marshmallow', 'party']
    assert kon.loads(kon.dumps(v2_list)) == v2_list
    v3_identifier_like = 'muhahaha'
    assert kon.dumps(v3_identifier_like) == v3_identifier_like
    assert kon.loads(kon.dumps(v3_identifier_like)) == v3_identifier_like
    v4_complex_str = '/path/to/file'
    assert kon.loads(kon.dumps(v4_complex_str)) == v4_complex_str
