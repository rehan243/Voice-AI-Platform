import pytest
from audio_processing import normalize_audio, trim_silence

def test_normalize_audio():
    # testing normalization of audio signal
    input_audio = [0.1, 0.2, 0.3, 0.4, 0.5]
    expected_output = [0.0, 0.2, 0.4, 0.6, 0.8]  # just a mock expected value
    normalized_audio = normalize_audio(input_audio)
    
    # assert that the normalized audio is as expected
    assert normalized_audio == expected_output

def test_trim_silence():
    # testing trimming silence from audio
    input_audio = [0, 0, 0, 0.5, 0.5, 0, 0]
    expected_output = [0.5, 0.5]  # mock expected value after trimming
    trimmed_audio = trim_silence(input_audio)
    
    # assert that the trimmed audio is as expected
    assert trimmed_audio == expected_output

# TODO: add more tests for edge cases and different audio inputs