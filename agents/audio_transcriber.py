
"""
Audio Transcriber Agent
Converts audio files to MIDI using Basic Pitch
"""

import numpy as np
from typing import Dict, Any
from pathlib import Path


class AudioTranscriber:
    """Transcribes audio to MIDI using Basic Pitch"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._load_model()
    
    def _load_model(self):
        """Load Basic Pitch model"""
        try:
            from basic_pitch.inference import predict
            from basic_pitch import ICASSP_2022_MODEL_PATH
            self.predict = predict
            self.model_path = ICASSP_2022_MODEL_PATH
            print("Basic Pitch model loaded")
        except ImportError:
            raise ImportError("basic-pitch not installed. Run: pip install basic-pitch")
    
    def transcribe(self, audio_path: str, output_path: str = "output.mid") -> Dict[str, Any]:
        """
        Transcribe audio to MIDI
        
        Args:
            audio_path: Input audio file
            output_path: Output MIDI file
            
        Returns:
            Dictionary with transcription results
        """
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"Transcribing: {audio_path}")
        
        # Get parameters
        onset_threshold = self.config.get("parameters", {}).get("onset_threshold", 0.5)
        frame_threshold = self.config.get("parameters", {}).get("frame_threshold", 0.3)
        
        # Run inference
        model_output, midi_data, note_events = self.predict(
            audio_path,
            self.model_path,
            onset_threshold=onset_threshold,
            frame_threshold=frame_threshold
        )
        
        # Save MIDI
        midi_data.write(output_path)
        
        # Calculate confidence (based on note activations)
        confidence = float(np.mean(model_output["note"]) if len(model_output["note"]) > 0 else 0.0)
        
        return {
            "success": True,
            "midi_path": output_path,
            "audio_path": audio_path,
            "confidence": confidence,
            "num_notes": len(note_events)
        }
