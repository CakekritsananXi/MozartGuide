
"""
Unit tests for ImageAnalyzer agent
Tests image analysis and music description generation
"""

import os
import pytest
from pathlib import Path
from PIL import Image
import io
import base64

from agents.image_analyzer import ImageAnalyzer


@pytest.fixture
def image_analyzer():
    """Initialize ImageAnalyzer with test configuration"""
    config = {
        "provider": "openai",
        "model": "gpt-4-vision",
        "system_prompt": "You are an expert music composer analyzing images.",
        "parameters": {
            "temperature": 0.7,
            "max_tokens": 500
        }
    }
    # Skip if no API key available
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
    return ImageAnalyzer(config)


@pytest.fixture
def test_image():
    """Create a simple test image"""
    # Create a 512x512 test image with gradient
    img = Image.new('RGB', (512, 512))
    pixels = img.load()
    for i in range(512):
        for j in range(512):
            pixels[i, j] = (i % 256, j % 256, (i + j) % 256)
    
    # Save to BytesIO
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Save to temporary file
    test_path = Path("test_image.png")
    img.save(test_path)
    
    yield test_path
    
    # Cleanup
    if test_path.exists():
        test_path.unlink()


class TestImageAnalyzer:
    """Test suite for ImageAnalyzer"""
    
    def test_initialization(self, image_analyzer):
        """Test that ImageAnalyzer initializes correctly"""
        assert image_analyzer is not None
        assert image_analyzer.provider == "openai"
        assert image_analyzer.model == "gpt-4-vision"
        assert hasattr(image_analyzer, 'client')
    
    def test_encode_image(self, image_analyzer, test_image):
        """Test image encoding to base64"""
        encoded = image_analyzer._encode_image(str(test_image))
        assert encoded is not None
        assert isinstance(encoded, str)
        assert len(encoded) > 0
        
        # Verify it's valid base64
        try:
            decoded = base64.b64decode(encoded)
            assert len(decoded) > 0
        except Exception as e:
            pytest.fail(f"Invalid base64 encoding: {e}")
    
    def test_analyze_basic(self, image_analyzer, test_image):
        """Test basic image analysis without user guidance"""
        description = image_analyzer.analyze(str(test_image))
        
        assert description is not None
        assert isinstance(description, str)
        assert len(description) > 10  # Should be substantial
        print(f"\n✓ Generated description: {description[:100]}...")
    
    def test_analyze_with_guidance(self, image_analyzer, test_image):
        """Test image analysis with user guidance"""
        user_guidance = "Focus on creating upbeat, energetic music"
        description = image_analyzer.analyze(
            str(test_image),
            user_guidance=user_guidance
        )
        
        assert description is not None
        assert isinstance(description, str)
        # Check if guidance influenced the description
        assert any(word in description.lower() for word in ['upbeat', 'energetic', 'energy', 'tempo'])
        print(f"\n✓ Guided description: {description[:100]}...")
    
    def test_analyze_nonexistent_file(self, image_analyzer):
        """Test handling of nonexistent image file"""
        with pytest.raises(FileNotFoundError):
            image_analyzer.analyze("nonexistent_image.jpg")
    
    def test_multiple_analyses_consistency(self, image_analyzer, test_image):
        """Test that multiple analyses of same image are consistent"""
        desc1 = image_analyzer.analyze(str(test_image))
        desc2 = image_analyzer.analyze(str(test_image))
        
        # Descriptions may vary but should have similar length/structure
        assert abs(len(desc1) - len(desc2)) < 200
        print(f"\n✓ Consistency check passed (lengths: {len(desc1)}, {len(desc2)})")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
