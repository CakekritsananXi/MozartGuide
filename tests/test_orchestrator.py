
"""
Integration tests for MusicOrchestrator
Tests complete pipelines and workflows
"""

import pytest
import os
from pathlib import Path
from PIL import Image
import io

from music_generator import MusicOrchestrator


@pytest.fixture
def orchestrator():
    """Initialize MusicOrchestrator"""
    # Set test mode for faster execution
    os.environ["TEST_MODE"] = "false"
    return MusicOrchestrator("mcp.json")


@pytest.fixture
def test_image(tmp_path):
    """Create a colorful test image"""
    img = Image.new('RGB', (512, 512))
    pixels = img.load()
    
    # Create a sunset-like gradient
    for i in range(512):
        for j in range(512):
            r = int(255 * (1 - j/512))  # Red gradient
            g = int(100 * (j/512))      # Green gradient
            b = int(50 * (i/512))       # Blue gradient
            pixels[i, j] = (r, g, b)
    
    test_path = tmp_path / "sunset.png"
    img.save(test_path)
    return test_path


class TestMusicOrchestrator:
    """Test suite for MusicOrchestrator"""
    
    def test_initialization(self, orchestrator):
        """Test orchestrator initializes correctly"""
        assert orchestrator is not None
        assert hasattr(orchestrator, 'config')
        assert hasattr(orchestrator, 'llm_client')
        print("\n✓ Orchestrator initialized")
    
    def test_generate_from_image_basic(self, orchestrator, test_image, tmp_path):
        """Test complete image-to-music pipeline"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
            
        output_file = tmp_path / "generated_music.wav"
        
        result = orchestrator.generate_from_image(
            image_path=str(test_image),
            duration=5,
            guidance_scale=3.5,
            output_path=str(output_file)
        )
        
        assert result["success"] is True
        assert "image_description" in result
        assert "music_description" in result
        assert Path(result["audio_path"]).exists()
        
        print(f"\n✓ Image-to-music pipeline completed")
        print(f"  Image description: {result['image_description'][:100]}...")
        print(f"  Music prompt: {result['music_description'][:100]}...")
        print(f"  Output: {result['audio_path']}")
    
    def test_generate_from_image_with_user_prompt(self, orchestrator, test_image, tmp_path):
        """Test image-to-music with user guidance"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
            
        output_file = tmp_path / "guided_music.wav"
        
        result = orchestrator.generate_from_image(
            image_path=str(test_image),
            user_prompt="Create relaxing meditation music",
            duration=5,
            output_path=str(output_file)
        )
        
        assert result["success"] is True
        assert result["user_prompt"] == "Create relaxing meditation music"
        # User prompt should influence the music description
        assert "relax" in result["music_description"].lower() or "calm" in result["music_description"].lower()
        
        print(f"\n✓ User-guided generation completed")
        print(f"  Music prompt: {result['music_description'][:100]}...")
    
    def test_generate_from_text(self, orchestrator, tmp_path):
        """Test direct text-to-music generation"""
        output_file = tmp_path / "text_music.wav"
        
        result = orchestrator.generate_from_text(
            prompt="Energetic rock music with electric guitar",
            duration=5,
            guidance_scale=4.0,
            output_path=str(output_file)
        )
        
        assert result["success"] is True
        assert Path(result["audio_path"]).exists()
        assert result["duration"] == 5
        
        print(f"\n✓ Text-to-music generation completed")
        print(f"  Output: {result['audio_path']}")
    
    def test_qwen_prompt_conversion(self, orchestrator):
        """Test Qwen Coder LLM prompt conversion"""
        if not orchestrator.llm_client:
            pytest.skip("Qwen LLM not configured")
            
        image_description = "A peaceful mountain landscape at sunrise with mist in the valleys"
        
        music_prompt = orchestrator._convert_description_to_music_prompt(image_description)
        
        assert music_prompt is not None
        assert isinstance(music_prompt, str)
        assert len(music_prompt) > len(image_description)  # Should be enhanced
        
        # Should contain music-related terms
        music_terms = ['music', 'tempo', 'mood', 'instrument', 'atmosphere', 'tone', 'melody', 'rhythm']
        assert any(term in music_prompt.lower() for term in music_terms)
        
        print(f"\n✓ Qwen conversion:")
        print(f"  Input: {image_description}")
        print(f"  Output: {music_prompt[:150]}...")
    
    def test_multiple_images_batch(self, orchestrator, tmp_path):
        """Test processing multiple images"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
            
        # Create multiple test images
        images = []
        for i, color in enumerate(['red', 'blue', 'green']):
            img = Image.new('RGB', (256, 256), color)
            img_path = tmp_path / f"{color}.png"
            img.save(img_path)
            images.append(img_path)
        
        results = []
        for idx, img_path in enumerate(images):
            output_file = tmp_path / f"music_{idx}.wav"
            result = orchestrator.generate_from_image(
                image_path=str(img_path),
                duration=5,
                output_path=str(output_file)
            )
            results.append(result)
        
        assert len(results) == 3
        assert all(r["success"] for r in results)
        
        print(f"\n✓ Batch processing completed: {len(results)} images")
        for idx, result in enumerate(results):
            print(f"  {idx+1}. {Path(result['audio_path']).name}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
