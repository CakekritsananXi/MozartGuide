
"""
Music Generator Agent
Generates audio from text prompts using MusicGen
"""

import torch
from typing import Dict, Any, Optional
import scipy.io.wavfile as wavfile
import numpy as np


class MusicGenerator:
    """Generates music from text prompts using MusicGen"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get("model_name", "facebook/musicgen-small")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self._load_model()
    
    def _load_model(self):
        """Load MusicGen model"""
        try:
            from audiocraft.models import MusicGen
            print(f"Loading MusicGen model: {self.model_name}")
            self.model = MusicGen.get_pretrained(self.model_name, device=self.device)
            print(f"Model loaded on {self.device}")
        except ImportError:
            raise ImportError("audiocraft not installed. Run: pip install audiocraft")
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    
    def generate(self, 
                prompt: str,
                duration: int = 10,
                guidance_scale: float = 3.5,
                temperature: float = 1.0,
                output_path: str = "output.wav") -> Dict[str, Any]:
        """
        Generate music from text prompt
        
        Args:
            prompt: Music description
            duration: Length in seconds
            guidance_scale: How closely to follow prompt (1.0-10.0)
            temperature: Randomness (0.1-2.0)
            output_path: Output file path
            
        Returns:
            Dictionary with generation results
        """
        # Set generation parameters
        self.model.set_generation_params(
            duration=duration,
            temperature=temperature,
            cfg_coef=guidance_scale
        )
        
        # Generate
        print(f"Generating music: {prompt[:60]}...")
        with torch.no_grad():
            wav = self.model.generate([prompt])
        
        # Convert to numpy and save
        audio_array = wav[0].cpu().numpy()
        
        # Ensure correct shape (samples,) or (channels, samples)
        if audio_array.ndim == 2:
            audio_array = audio_array.squeeze(0)
        
        # Normalize to int16 range
        audio_array = (audio_array * 32767).astype(np.int16)
        
        # Save
        sample_rate = self.model.sample_rate
        wavfile.write(output_path, sample_rate, audio_array)
        
        return {
            "success": True,
            "audio_path": output_path,
            "prompt": prompt,
            "duration": duration,
            "sample_rate": sample_rate,
            "guidance_scale": guidance_scale,
            "temperature": temperature
        }
