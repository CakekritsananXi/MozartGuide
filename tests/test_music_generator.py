
"""
Unit tests for MusicGenerator agent
Tests music generation from text prompts
"""

import pytest
import os
from pathlib import Path
import wave
import numpy as np

from agents.music_generator import MusicGenerator


@pytest.fixture
def music_generator():
    """Initialize MusicGenerator with small model for testing"""
    config = {
        "model_name": "facebook/musicgen-small",
        "parameters": {
            "duration": 5,  # Short duration for tests
            "guidance_scale": 3.0,
            "temperature": 1.0
        }
    }
    return MusicGenerator(config)


class TestMusicGenerator:
    """Test suite for MusicGenerator"""
    
    def test_initialization(self, music_generator):
        """Test that MusicGenerator initializes correctly"""
        assert music_generator is not None
        assert hasattr(music_generator, 'model')
        assert hasattr(music_generator, 'device')
        print(f"\n✓ Model loaded on device: {music_generator.device}")
    
    def test_generate_basic(self, music_generator, tmp_path):
        """Test basic music generation"""
        prompt = "Calm ambient music with soft piano"
        output_file = tmp_path / "test_output.wav"
        
        result = music_generator.generate(
            prompt=prompt,
            duration=5,
            output_path=str(output_file)
        )
        
        assert result["success"] is True
        assert Path(result["audio_path"]).exists()
        assert result["duration"] == 5
        assert result["prompt"] == prompt
        
        # Verify audio file is valid
        with wave.open(str(output_file), 'rb') as wav:
            assert wav.getnchannels() in [1, 2]
            assert wav.getsampwidth() == 2  # 16-bit
            assert wav.getframerate() > 0
            
        print(f"\n✓ Generated {result['duration']}s audio: {result['audio_path']}")
    
    def test_generate_different_durations(self, music_generator, tmp_path):
        """Test generation with different durations"""
        prompt = "Upbeat electronic music"
        durations = [5, 10]
        
        for duration in durations:
            output_file = tmp_path / f"test_{duration}s.wav"
            result = music_generator.generate(
                prompt=prompt,
                duration=duration,
                output_path=str(output_file)
            )
            
            assert result["success"] is True
            assert result["duration"] == duration
            
            # Check file size increases with duration
            file_size = Path(result["audio_path"]).stat().st_size
            assert file_size > 0
            print(f"\n✓ {duration}s audio: {file_size / 1024:.1f} KB")
    
    def test_generate_different_guidance(self, music_generator, tmp_path):
        """Test generation with different guidance scales"""
        prompt = "Jazz music with saxophone"
        guidance_scales = [2.0, 5.0]
        
        for guidance in guidance_scales:
            output_file = tmp_path / f"test_guidance_{guidance}.wav"
            result = music_generator.generate(
                prompt=prompt,
                duration=5,
                guidance_scale=guidance,
                output_path=str(output_file)
            )
            
            assert result["success"] is True
            assert result["guidance_scale"] == guidance
            print(f"\n✓ Generated with guidance {guidance}")
    
    def test_generate_different_temperatures(self, music_generator, tmp_path):
        """Test generation with different temperature values"""
        prompt = "Classical orchestral music"
        temperatures = [0.8, 1.2]
        
        for temp in temperatures:
            output_file = tmp_path / f"test_temp_{temp}.wav"
            result = music_generator.generate(
                prompt=prompt,
                duration=5,
                temperature=temp,
                output_path=str(output_file)
            )
            
            assert result["success"] is True
            assert result["temperature"] == temp
            print(f"\n✓ Generated with temperature {temp}")
    
    def test_audio_quality(self, music_generator, tmp_path):
        """Test that generated audio meets quality standards"""
        output_file = tmp_path / "quality_test.wav"
        
        result = music_generator.generate(
            prompt="High quality orchestral music",
            duration=5,
            output_path=str(output_file)
        )
        
        # Read and analyze audio
        with wave.open(str(output_file), 'rb') as wav:
            frames = wav.readframes(wav.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Check for silence (all zeros)
            assert not np.all(audio_data == 0), "Audio is silent"
            
            # Check dynamic range
            assert audio_data.max() > 1000, "Audio has very low amplitude"
            
            # Check sample rate
            assert wav.getframerate() == result["sample_rate"]
            
        print(f"\n✓ Audio quality checks passed")
        print(f"  Sample rate: {result['sample_rate']} Hz")
        print(f"  Dynamic range: {audio_data.max() - audio_data.min()}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
