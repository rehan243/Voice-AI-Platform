import pytest
from audio_processing import preprocess_audio, extract_features

def test_preprocess_audio():
    # testing audio preprocessing on a sample audio file
    input_audio = 'tests/sample_audio.wav'
    expected_output = 'tests/preprocessed_audio.wav'
    
    processed_audio = preprocess_audio(input_audio)
    
    # check if the output file is created
    assert processed_audio == expected_output
    # TODO: add more checks for audio quality

def test_extract_features():
    # testing feature extraction from preprocessed audio
    input_audio = 'tests/preprocessed_audio.wav'
    expected_features_shape = (10, 128)  # assuming we expect 10 frames and 128 features

    features = extract_features(input_audio)
    
    # check if the shape of extracted features is as expected
    assert features.shape == expected_features_shape
    # TODO: add checks for feature values if needed

def test_preprocess_audio_invalid_input():
    # testing how preprocess_audio handles invalid input
    invalid_audio = 'tests/invalid_audio.txt'
    
    with pytest.raises(ValueError):
        preprocess_audio(invalid_audio)