import pytest
from audio_processing import normalize_audio, trim_silence

def test_normalize_audio():
    # testing normalization of audio signal
    input_audio = [0.1, 0.5, 0.3, 0.7]
    expected_output = [0.14285714, 0.71428571, 0.42857143, 1.0]  # normalized values
    output_audio = normalize_audio(input_audio)
    
    # simple assert to check if output is as expected
    assert all(abs(a - b) < 1e-5 for a, b in zip(output_audio, expected_output))

def test_trim_silence():
    # testing trimming silence from audio
    input_audio = [0, 0, 0, 0.5, 0.7, 0, 0]
    expected_output = [0.5, 0.7]  # expected to trim leading and trailing silence
    output_audio = trim_silence(input_audio)
    
    assert output_audio == expected_output

def test_trim_silence_no_silence():
    # testing when there's no silence to trim
    input_audio = [0.1, 0.2, 0.3]
    expected_output = [0.1, 0.2, 0.3]
    output_audio = trim_silence(input_audio)

    assert output_audio == expected_output

# TODO: add more tests for edge cases and different audio formats