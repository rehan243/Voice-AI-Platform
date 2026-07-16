import pytest
from audio_processing import normalize_audio, trim_silence

# test normalize_audio function
def test_normalize_audio():
    # simple case with a known input and output
    input_audio = [0.2, 0.5, 0.8]
    expected_output = [0.25, 0.625, 1.0]  # assuming normalize scales to max 1.0
    result = normalize_audio(input_audio)
    assert result == expected_output

# test trim_silence function
def test_trim_silence():
    # input with leading and trailing silence
    input_audio = [0.0, 0.0, 0.3, 0.5, 0.0, 0.0]
    expected_output = [0.3, 0.5]  # silence should be trimmed
    result = trim_silence(input_audio)
    assert result == expected_output

# TODO: add more tests for edge cases
def test_trim_silence_edge_case():
    # input with no silence at all
    input_audio = [0.1, 0.2, 0.3]
    expected_output = [0.1, 0.2, 0.3]  # should return the same
    result = trim_silence(input_audio)
    assert result == expected_output

# test with all silence
def test_trim_silence_all_silence():
    input_audio = [0.0, 0.0, 0.0]
    expected_output = []  # should return empty list
    result = trim_silence(input_audio)
    assert result == expected_output