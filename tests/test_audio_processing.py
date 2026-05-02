import pytest
from audio_processing import normalize_audio, trim_silence

def test_normalize_audio():
    # testing normalization on a sample audio signal
    audio_input = [0.1, 0.5, 0.9, 0.2, 0.3]
    normalized_audio = normalize_audio(audio_input)
    
    # check if the max value is 1.0 after normalization
    assert max(normalized_audio) == 1.0
    # check if the min value is 0.0 after normalization
    assert min(normalized_audio) == 0.0

def test_trim_silence():
    # testing silence trimming on a sample audio signal
    audio_input = [0.0, 0.0, 0.5, 0.6, 0.0, 0.0]
    trimmed_audio = trim_silence(audio_input)
    
    # check if the trimmed audio is as expected
    expected_output = [0.5, 0.6]
    assert trimmed_audio == expected_output

def test_trim_silence_no_silence():
    # testing trimming when there's no silence
    audio_input = [0.5, 0.6, 0.7]
    trimmed_audio = trim_silence(audio_input)
    
    # ensure output is same as input if no silence
    assert trimmed_audio == audio_input

# TODO: add more tests for edge cases and different audio formats