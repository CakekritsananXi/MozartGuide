"""
Phin Isan AI - Main CLI Entry Point
Command-line interface for music generation
"""

import argparse
import sys
import os
from pathlib import Path
from music_generator import MusicOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description="Phin Isan AI - Music Generation Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate music from image
  python main.py --image sunset.jpg --output music.wav --duration 15

  # Generate from text prompt
  python main.py --prompt "Calm ambient music" --output ambient.wav

  # Convert audio to MIDI
  python main.py --audio song.wav --midi-output notes.mid

  # Test mode (no models loaded)
  python main.py --image test.jpg --test-mode
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--image", type=str, help="Path to input image")
    input_group.add_argument("--prompt", type=str, help="Text prompt for music generation")
    input_group.add_argument("--audio", type=str, help="Audio file to transcribe to MIDI")
    
    # Output options
    parser.add_argument("--output", type=str, default="output.wav", 
                       help="Output audio file path (default: output.wav)")
    parser.add_argument("--midi-output", type=str, default="output.mid",
                       help="Output MIDI file path (default: output.mid)")
    
    # Generation parameters
    parser.add_argument("--duration", type=int, default=10,
                       help="Music duration in seconds (default: 10)")
    parser.add_argument("--guidance", type=float, default=3.5,
                       help="Guidance scale 1.0-10.0 (default: 3.5)")
    parser.add_argument("--user-prompt", type=str,
                       help="Additional guidance for image-to-music")
    
    # Configuration
    parser.add_argument("--config", type=str, default="mcp.json",
                       help="Configuration file (default: mcp.json)")
    parser.add_argument("--test-mode", action="store_true",
                       help="Run in test mode without loading models")
    parser.add_argument("--use-agent-router", action="store_true",
                       help="Use Agent Router for orchestration")
    
    # Utility
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Set test mode
    if args.test_mode:
        os.environ["TEST_MODE"] = "true"
        print("🧪 Running in TEST MODE (no models will be loaded)")
    
    # Initialize orchestrator
    try:
        orchestrator = MusicOrchestrator(
            config_path=args.config,
            use_agent_router=args.use_agent_router
        )
    except Exception as e:
        print(f"❌ Error initializing orchestrator: {e}")
        return 1
    
    # Execute based on input type
    try:
        if args.image:
            # Image-to-music pipeline
            print(f"🖼️  Processing image: {args.image}")
            result = orchestrator.generate_from_image(
                image_path=args.image,
                user_prompt=args.user_prompt,
                duration=args.duration,
                guidance_scale=args.guidance,
                output_path=args.output
            )
            
            print(f"\n✅ Music generated successfully!")
            print(f"📝 Description: {result.get('music_description', 'N/A')}")
            print(f"🎵 Output: {result.get('audio_path', 'N/A')}")
            print(f"⏱️  Duration: {result.get('duration', 0)} seconds")
            
        elif args.prompt:
            # Text-to-music generation
            print(f"📝 Generating from prompt: {args.prompt[:50]}...")
            result = orchestrator.generate_from_text(
                prompt=args.prompt,
                duration=args.duration,
                guidance_scale=args.guidance,
                output_path=args.output
            )
            
            print(f"\n✅ Music generated successfully!")
            print(f"🎵 Output: {result.get('audio_path', 'N/A')}")
            print(f"⏱️  Duration: {result.get('duration', 0)} seconds")
            
        elif args.audio:
            # Audio-to-MIDI transcription
            print(f"🎼 Transcribing audio: {args.audio}")
            result = orchestrator.transcribe_audio(
                audio_path=args.audio,
                output_path=args.midi_output
            )
            
            print(f"\n✅ Transcription completed!")
            print(f"🎹 MIDI output: {result.get('midi_path', 'N/A')}")
            print(f"📊 Confidence: {result.get('confidence', 0):.2%}")
        
        if args.verbose:
            import json
            print(f"\n📋 Full result:")
            print(json.dumps(result, indent=2))
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
