
"""
Tests using real-world data and scenarios
"""

import pytest
import os
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO

from music_generator import MusicOrchestrator


@pytest.fixture
def orchestrator():
    """Initialize orchestrator"""
    return MusicOrchestrator("mcp.json")


class TestRealWorldScenarios:
    """Test suite with real-world use cases"""
    
    @pytest.mark.slow
    def test_nature_photography(self, orchestrator, tmp_path):
        """Test with nature/landscape photography scenario"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        # Create a nature-like image (forest green with sky blue)
        img = Image.new('RGB', (1024, 768))
        pixels = img.load()
        for i in range(1024):
            for j in range(768):
                if j < 256:  # Sky
                    pixels[i, j] = (135, 206, 235)
                else:  # Forest
                    pixels[i, j] = (34, 139, 34)
        
        img_path = tmp_path / "nature.jpg"
        img.save(img_path)
        output_path = tmp_path / "nature_music.wav"
        
        result = orchestrator.generate_from_image(
            image_path=str(img_path),
            user_prompt="peaceful and natural",
            duration=10,
            guidance_scale=3.5,
            output_path=str(output_path)
        )
        
        assert result["success"] is True
        # Check for nature/calm related terms in description
        desc_lower = result["music_description"].lower()
        nature_terms = ['calm', 'peaceful', 'natural', 'serene', 'ambient', 'gentle']
        assert any(term in desc_lower for term in nature_terms)
        
        print(f"\n✓ Nature photography test:")
        print(f"  Description: {result['music_description'][:150]}...")
    
    @pytest.mark.slow
    def test_urban_cityscape(self, orchestrator, tmp_path):
        """Test with urban/city scenario"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        # Create an urban-like image (dark with neon colors)
        img = Image.new('RGB', (800, 600))
        pixels = img.load()
        for i in range(800):
            for j in range(600):
                # Dark background with neon accents
                if i % 100 < 10:  # Neon lines
                    pixels[i, j] = (255, 0, 255)
                else:
                    pixels[i, j] = (20, 20, 40)
        
        img_path = tmp_path / "city.jpg"
        img.save(img_path)
        output_path = tmp_path / "city_music.wav"
        
        result = orchestrator.generate_from_image(
            image_path=str(img_path),
            user_prompt="energetic urban atmosphere",
            duration=10,
            output_path=str(output_path)
        )
        
        assert result["success"] is True
        desc_lower = result["music_description"].lower()
        urban_terms = ['energetic', 'urban', 'electronic', 'beat', 'rhythm', 'dynamic']
        assert any(term in desc_lower for term in urban_terms)
        
        print(f"\n✓ Urban cityscape test:")
        print(f"  Description: {result['music_description'][:150]}...")
    
    def test_music_genre_prompts(self, orchestrator, tmp_path):
        """Test different music genre prompts"""
        genres = [
            ("Classical piano music with emotional depth", "classical"),
            ("Upbeat electronic dance music with synthesizers", "electronic"),
            ("Smooth jazz with saxophone and piano", "jazz"),
            ("Acoustic folk music with guitar", "folk"),
            ("Ambient meditation music with nature sounds", "ambient")
        ]
        
        for prompt, genre in genres:
            output_path = tmp_path / f"{genre}_music.wav"
            result = orchestrator.generate_from_text(
                prompt=prompt,
                duration=5,
                output_path=str(output_path)
            )
            
            assert result["success"] is True
            assert Path(result["audio_path"]).exists()
            
            # Check file size is reasonable
            file_size = Path(result["audio_path"]).stat().st_size
            assert file_size > 50000  # At least 50KB
            
            print(f"\n✓ {genre.capitalize()} music generated: {file_size/1024:.1f} KB")
    
    @pytest.mark.slow
    def test_different_image_sizes(self, orchestrator, tmp_path):
        """Test with various image dimensions"""
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY not set")
        
        sizes = [
            (256, 256, "small"),
            (512, 512, "medium"),
            (1024, 768, "large"),
            (1920, 1080, "hd")
        ]
        
        for width, height, size_name in sizes:
            img = Image.new('RGB', (width, height), color=(100, 150, 200))
            img_path = tmp_path / f"{size_name}_{width}x{height}.jpg"
            img.save(img_path)
            
            output_path = tmp_path / f"{size_name}_music.wav"
            result = orchestrator.generate_from_image(
                image_path=str(img_path),
                duration=5,
                output_path=str(output_path)
            )
            
            assert result["success"] is True
            print(f"\n✓ {size_name} image ({width}x{height}) processed successfully")
    
    def test_duration_variations(self, orchestrator, tmp_path):
        """Test different music durations"""
        durations = [5, 10, 15, 20, 30]
        prompt = "Atmospheric ambient music"
        
        for duration in durations:
            output_path = tmp_path / f"music_{duration}s.wav"
            result = orchestrator.generate_from_text(
                prompt=prompt,
                duration=duration,
                output_path=str(output_path)
            )
            
            assert result["success"] is True
            assert result["duration"] == duration
            
            # Verify file size scales with duration
            file_size = Path(result["audio_path"]).stat().st_size
            expected_min_size = duration * 10000  # Rough estimate
            assert file_size > expected_min_size
            
            print(f"\n✓ {duration}s music: {file_size/1024:.1f} KB")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
