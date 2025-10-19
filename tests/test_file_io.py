import kon


def test_dump_then_read_then_loads(tmp_path):
    val = {'I': {'am': 'a'}, 4: 'leaf clover'}
    with (tmp_path / "test_file.kon").open("w") as fp:
        kon.dump(val, fp)
    with (tmp_path / "test_file.kon").open("rb") as fp:
        v2 = kon.loads(fp.read())
    assert val == v2

def test_dump_then_load_file_io(tmp_path):
    val = {'I': {'am': 'a'}, 5: ['leaf lucky', 'clover']}
    with (tmp_path / "test_file.kon").open("w") as fp:
        kon.dump(val, fp)
    with (tmp_path / "test_file.kon").open("r") as fp:
        v2 = kon.load(fp)
    assert val == v2
