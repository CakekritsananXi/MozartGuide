
"""
Image Analyzer Agent
Converts images to music descriptions using vision-language models
"""

import os
import base64
from typing import Optional, Dict, Any
from pathlib import Path


class ImageAnalyzer:
    """Analyzes images and generates music descriptions"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get("provider", "openai")
        self.model = config.get("model", "gpt-4-vision")
        
        # Initialize based on provider
        if self.provider == "openai":
            self._init_openai()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze(self, image_path: str, user_guidance: Optional[str] = None) -> str:
        """
        Analyze image and generate music description
        
        Args:
            image_path: Path to image file
            user_guidance: Optional user prompt to guide analysis
            
        Returns:
            Music description string
        """
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Encode image
        base64_image = self._encode_image(image_path)
        
        # Build prompt
        system_prompt = self.config.get("system_prompt", 
            "You are an expert music composer. Analyze images and create detailed "
            "music generation prompts that capture mood, atmosphere, and visual essence."
        )
        
        user_prompt = "Analyze this image and create a detailed music generation prompt. "
        if user_guidance:
            user_prompt += f"User guidance: {user_guidance}. "
        user_prompt += "Focus on: mood, tempo, instruments, genre, and atmosphere."
        
        # Call API
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=self.config.get("parameters", {}).get("max_tokens", 500),
            temperature=self.config.get("parameters", {}).get("temperature", 0.7)
        )
        
        return response.choices[0].message.content
