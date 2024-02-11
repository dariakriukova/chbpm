import pytest
from chbpm.bpm import analyze_bpm

test_cases = [
    ('tests/data/60.m4a', 60),
    ('tests/data/70.m4a', 70),
    ('tests/data/90.m4a', 90),
    ('tests/data/100.m4a', 100),
    ('tests/data/120.m4a', 120),
    ('tests/data/180.m4a', 180),
]

@pytest.mark.parametrize("file_path, expected_bpm", test_cases)
def test_analyze_bpm_known_file(file_path, expected_bpm):
    bpm = analyze_bpm(file_path, 180)
    assert bpm == pytest.approx(expected_bpm, .03)