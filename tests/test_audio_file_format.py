import pytest
from chbpm.bpm import analyze_bpm

test_cases = [
    ('tests/data/aac.aac', 85),
    ('tests/data/aiff.aiff', 85),
    ('tests/data/flac.flac', 85),
    ('tests/data/m4a.m4a', 85),
    ('tests/data/wav.wav', 85),
    ('tests/data/wma.wma', 80),
]

@pytest.mark.parametrize("file_path, expected_bpm", test_cases)
def test_audio_format_and_bpm_consistency(file_path, expected_bpm):
    detected_bpm = analyze_bpm(file_path, expected_bpm)
    assert detected_bpm == pytest.approx(expected_bpm, .03)
