import pytest
from audio_processing import normalize_audio, trim_silence

# testing the normalize_audio function
def test_normalize_audio():
    audio_input = [0.1, 0.5, 0.2, -0.1, -0.5]  # example audio samples
    normalized = normalize_audio(audio_input)
    
    # check if the normalized audio is within the expected range
    assert all(-1 <= sample <= 1 for sample in normalized)
    assert len(normalized) == len(audio_input)

# testing the trim_silence function
def test_trim_silence():
    audio_input = [0, 0, 0.2, 0.3, 0, 0, 0.1, 0]  # audio with leading/trailing silence
    trimmed = trim_silence(audio_input)
    
    # check if the trimmed audio has no leading or trailing silence
    assert trimmed[0] != 0
    assert trimmed[-1] != 0
    assert len(trimmed) < len(audio_input)  # should be shorter than the input

# TODO: add more tests for edge cases and different audio formats