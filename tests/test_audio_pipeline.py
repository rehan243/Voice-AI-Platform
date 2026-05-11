import pytest
from audio_pipeline import AudioProcessor

# testing audio processor behavior
def test_audio_processing():
    processor = AudioProcessor()

    # test basic audio processing
    input_audio = "path/to/input.wav"
    expected_output = "path/to/expected_output.wav"

    output_audio = processor.process(input_audio)
    
    assert output_audio == expected_output, f"Expected {expected_output}, but got {output_audio}"

def test_audio_normalization():
    processor = AudioProcessor()

    # test audio normalization
    input_audio = "path/to/loud_audio.wav"
    normalized_audio = processor.normalize(input_audio)

    assert processor.is_normalized(normalized_audio), "Audio should be normalized"

def test_audio_format_conversion():
    processor = AudioProcessor()

    # test format conversion
    input_audio = "path/to/audio.mp3"
    expected_output = "path/to/audio.wav"

    output_audio = processor.convert_format(input_audio, 'wav')
    
    assert output_audio == expected_output, f"Expected {expected_output}, but got {output_audio}"

# TODO: add more tests for edge cases and exceptions