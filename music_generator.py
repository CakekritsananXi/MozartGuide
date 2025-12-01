
"""
Music Generation Orchestrator for Phin Isan AI
Implements the core pipeline for image-to-music and audio processing
"""

import os
import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
import logging

# Import real agents
from agents.image_analyzer import ImageAnalyzer
from agents.music_generator import MusicGenerator
from agents.audio_transcriber import AudioTranscriber

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MusicConfig:
    """Load and manage configuration from mcp.json"""
    
    def __init__(self, config_path: str = "mcp.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from mcp.json"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {self.config_path} not found")
            return {}
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Get configuration for specific agent"""
        return self.config.get("agents", {}).get(agent_name, {})
    
    def get_model_config(self, model_type: str, model_name: str) -> Dict[str, Any]:
        """Get model configuration"""
        return self.config.get("models", {}).get(model_type, {}).get(model_name, {})


class ImageToMusicAgent:
    """Agent for converting images to music prompts"""
    
    def __init__(self, config: MusicConfig):
        self.config = config.get_agent_config("image_to_music")
        self.test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
        
        if not self.test_mode:
            self.analyzer = ImageAnalyzer(self.config)
    
    def analyze_image(self, image_path: str, user_prompt: Optional[str] = None) -> str:
        """
        Analyze image and generate music description
        
        Args:
            image_path: Path to input image
            user_prompt: Optional user guidance
            
        Returns:
            Music generation prompt
        """
        if self.test_mode:
            return self._mock_analysis(image_path, user_prompt)
        
        logger.info(f"Analyzing image: {image_path}")
        return self.analyzer.analyze(image_path, user_prompt)
    
    def _mock_analysis(self, image_path: str, user_prompt: Optional[str]) -> str:
        """Mock analysis for testing"""
        base_prompt = "Calm ambient music with soft instrumentation"
        if user_prompt:
            return f"{base_prompt}, incorporating: {user_prompt}"
        return base_prompt
    
    def _template_based_prompt(self, image_path: str, user_prompt: Optional[str]) -> str:
        """Generate prompt using templates"""
        prompt_parts = []
        
        if user_prompt:
            prompt_parts.append(user_prompt)
        else:
            prompt_parts.append("Atmospheric music inspired by visual content")
        
        # Add quality indicators
        prompt_parts.extend([
            "high quality",
            "professional production",
            "clear instrumentation"
        ])
        
        return ", ".join(prompt_parts)


class TextToMusicAgent:
    """Agent for generating music from text prompts"""
    
    def __init__(self, config: MusicConfig):
        self.config = config.get_agent_config("text_to_music")
        self.test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
        
        if not self.test_mode:
            self.generator = MusicGenerator(self.config)
    
    def generate(self, prompt: str, duration: int = 10, 
                 guidance_scale: float = 3.5, 
                 output_path: str = "output.wav") -> Dict[str, Any]:
        """
        Generate music from text prompt
        
        Args:
            prompt: Music description
            duration: Length in seconds
            guidance_scale: How closely to follow the prompt
            output_path: Where to save the audio
            
        Returns:
            Dictionary with generation results
        """
        if self.test_mode:
            return self._mock_generation(prompt, duration, output_path)
        
        logger.info(f"Generating music: {prompt[:50]}...")
        return self.generator.generate(prompt, duration, guidance_scale, 1.0, output_path)
    
    def _mock_generation(self, prompt: str, duration: int, output_path: str) -> Dict[str, Any]:
        """Mock generation for testing"""
        logger.info(f"[TEST MODE] Mock generating: {prompt[:50]}...")
        return {
            "success": True,
            "audio_path": output_path,
            "prompt": prompt,
            "duration": duration,
            "test_mode": True
        }


class AudioToMIDIAgent:
    """Agent for converting audio to MIDI"""
    
    def __init__(self, config: MusicConfig):
        self.config = config.get_agent_config("audio_to_midi")
        self.test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
        
        if not self.test_mode:
            self.transcriber = AudioTranscriber(self.config)
    
    def transcribe(self, audio_path: str, output_path: str = "output.mid") -> Dict[str, Any]:
        """
        Transcribe audio to MIDI
        
        Args:
            audio_path: Input audio file
            output_path: Output MIDI file
            
        Returns:
            Dictionary with transcription results
        """
        if self.test_mode:
            return self._mock_transcription(audio_path, output_path)
        
        logger.info(f"Transcribing audio: {audio_path}")
        return self.transcriber.transcribe(audio_path, output_path)
    
    def _mock_transcription(self, audio_path: str, output_path: str) -> Dict[str, Any]:
        """Mock transcription for testing"""
        logger.info(f"[TEST MODE] Mock transcribing: {audio_path}")
        return {
            "success": True,
            "midi_path": output_path,
            "audio_path": audio_path,
            "confidence": 0.85,
            "test_mode": True
        }


class MusicOrchestrator:
    """Main orchestrator for all music generation workflows"""
    
    def __init__(self, config_path: str = "mcp.json"):
        self.config = MusicConfig(config_path)
        
        # Initialize agents
        self.image_to_music = ImageToMusicAgent(self.config)
        self.text_to_music = TextToMusicAgent(self.config)
        self.audio_to_midi = AudioToMIDIAgent(self.config)
        
        logger.info("Music Orchestrator initialized")
    
    def generate_from_image(self, image_path: str, 
                           user_prompt: Optional[str] = None,
                           duration: int = 10,
                           guidance_scale: float = 3.5,
                           output_path: str = "output.wav") -> Dict[str, Any]:
        """
        Complete pipeline: Image -> Description -> Music
        
        Args:
            image_path: Path to input image
            user_prompt: Optional user guidance
            duration: Music duration in seconds
            guidance_scale: Prompt adherence (1.0-10.0)
            output_path: Output audio file path
            
        Returns:
            Dictionary with all results
        """
        logger.info(f"Starting image-to-music pipeline for: {image_path}")
        
        # Step 1: Analyze image
        music_description = self.image_to_music.analyze_image(
            image_path, 
            user_prompt
        )
        
        # Step 2: Generate music
        music_result = self.text_to_music.generate(
            prompt=music_description,
            duration=duration,
            guidance_scale=guidance_scale,
            output_path=output_path
        )
        
        # Combine results
        result = {
            **music_result,
            "image_path": image_path,
            "music_description": music_description,
            "user_prompt": user_prompt
        }
        
        logger.info("Image-to-music pipeline completed")
        return result
    
    def generate_from_text(self, prompt: str, 
                          duration: int = 10,
                          guidance_scale: float = 3.5,
                          output_path: str = "output.wav") -> Dict[str, Any]:
        """
        Generate music directly from text prompt
        
        Args:
            prompt: Music description
            duration: Music duration in seconds
            guidance_scale: Prompt adherence (1.0-10.0)
            output_path: Output audio file path
            
        Returns:
            Dictionary with generation results
        """
        logger.info(f"Generating music from text: {prompt[:50]}...")
        
        return self.text_to_music.generate(
            prompt=prompt,
            duration=duration,
            guidance_scale=guidance_scale,
            output_path=output_path
        )
    
    def transcribe_audio(self, audio_path: str, 
                        output_path: str = "output.mid") -> Dict[str, Any]:
        """
        Convert audio to MIDI
        
        Args:
            audio_path: Input audio file
            output_path: Output MIDI file
            
        Returns:
            Dictionary with transcription results
        """
        logger.info(f"Transcribing audio to MIDI: {audio_path}")
        
        return self.audio_to_midi.transcribe(
            audio_path=audio_path,
            output_path=output_path
        )


# Example usage
if __name__ == "__main__":
    # Enable test mode
    os.environ["TEST_MODE"] = "true"
    
    # Create orchestrator
    orchestrator = MusicOrchestrator()
    
    # Test image-to-music
    result = orchestrator.generate_from_image(
        image_path="test_image.jpg",
        user_prompt="peaceful and uplifting",
        duration=15
    )
    print(json.dumps(result, indent=2))
    
    # Test text-to-music
    result = orchestrator.generate_from_text(
        prompt="Energetic electronic music with driving beats",
        duration=20
    )
    print(json.dumps(result, indent=2))
    
    # Test audio-to-midi
    result = orchestrator.transcribe_audio(
        audio_path="test_audio.wav"
    )
    print(json.dumps(result, indent=2))
