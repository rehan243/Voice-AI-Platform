import pytest
from audio_processing import normalize_audio, trim_silence  # assuming these are real functions

def test_normalize_audio():
    # test with a sample audio array
    audio_input = [0.1, 0.5, 0.3, -0.2, -0.5]
    normalized_audio = normalize_audio(audio_input)
    
    assert all(-1 <= sample <= 1 for sample in normalized_audio)  # check if normalized
    assert len(normalized_audio) == len(audio_input)  # length should stay the same

def test_trim_silence():
    # test with a sample audio array with silence
    audio_input = [0.0, 0.0, 0.1, 0.5, 0.0, 0.0]
    trimmed_audio = trim_silence(audio_input)
    
    assert trimmed_audio == [0.1, 0.5]  # expect silence trimmed
    assert len(trimmed_audio) < len(audio_input)  # length should reduce

def test_trim_silence_no_silence():
    audio_input = [0.1, 0.2, 0.3, 0.4]
    trimmed_audio = trim_silence(audio_input)

    assert trimmed_audio == audio_input  # no change if no silence
    assert len(trimmed_audio) == len(audio_input)  # length should stay the same