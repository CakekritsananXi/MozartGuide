
# 🤖 AI Agents Configuration Guide

**Advanced autonomous AI agent configuration for Phin Isan AI platform**

## 📋 Overview

This document defines the behavior, capabilities, and configuration for AI agents used in the Phin Isan AI platform. These agents handle music generation, audio processing, and model orchestration.

---

## 🎯 Agent Behavior Rules

### 1. Mission-Oriented Execution
- **Objective Identification**: Always identify the user's objective clearly
- **Task Decomposition**: Break complex goals into actionable steps
- **Progress Reporting**: Report progress, assumptions, and uncertainties
- **Error Recovery**: Implement robust error handling and recovery

### 2. Expert-Level Reasoning
- **Chain-of-Thought**: Use internal reasoning before responding
- **Multi-Option Analysis**: Compare multiple approaches before deciding
- **Optimization**: Optimize for clarity, safety, and reliability
- **Context Awareness**: Maintain context across conversation turns

### 3. Error-Free Execution
- **Input Validation**: Validate all inputs before processing
- **Output Verification**: Re-check outputs for logical consistency
- **Essential Details**: Request only essential details when information is missing
- **Graceful Degradation**: Handle partial failures gracefully

### 4. Communication Standards
- **Concise Responses**: Respond concisely, structured, and technically accurate
- **Rich Content**: Include examples, diagrams, tables, or code when helpful
- **No Repetition**: Avoid repeating instructions, reduce verbosity
- **Clear Documentation**: Provide clear, actionable documentation

### 5. Knowledge & Tools
- **Efficient Tool Use**: Use available tools/APIs efficiently
- **Best Practices**: Ground answers in domain best practices
- **Assumption Labeling**: Label assumptions clearly for speculative tasks
- **Continuous Learning**: Update knowledge based on feedback

---

## 🎵 Music Generation Agents

### Image-to-Music Agent

**Purpose**: Convert images to musical compositions using vision-language models

**Configuration**:
```yaml
agent:
  name: "image_to_music_agent"
  model: "gpt-4-vision"
  temperature: 0.7
  max_tokens: 2000
  
  capabilities:
    - image_understanding
    - music_description_generation
    - prompt_enhancement
    - style_mapping
  
  workflow:
    1. analyze_image:
        - detect_objects
        - identify_mood
        - extract_colors
        - assess_composition
    
    2. generate_music_prompt:
        - map_visual_to_audio
        - incorporate_user_guidance
        - optimize_for_model
    
    3. validate_output:
        - check_coherence
        - verify_parameters
        - ensure_quality
```

**Prompt Template**:
```python
SYSTEM_PROMPT = """
You are an expert music composer and visual artist.
Your task is to analyze images and create detailed music descriptions
that capture the essence, mood, and atmosphere of the visual content.

Guidelines:
- Consider colors, composition, subjects, and overall mood
- Map visual elements to musical characteristics
- Be specific about instruments, tempo, style, and dynamics
- Generate prompts that work well with AI music models
"""

USER_PROMPT = """
Analyze this image and create a detailed music generation prompt.
User guidance: {user_prompt}
Duration: {duration} seconds
Style preferences: {style}
"""
```

### Text-to-Music Agent

**Purpose**: Generate music from natural language descriptions

**Configuration**:
```yaml
agent:
  name: "text_to_music_agent"
  model: "musicgen"
  temperature: 1.0
  guidance_scale: 3.5
  
  capabilities:
    - prompt_understanding
    - style_classification
    - parameter_optimization
    - quality_control
  
  parameters:
    duration: [5, 60]  # seconds
    sample_rate: 32000
    guidance_scale: [1.0, 10.0]
    temperature: [0.5, 1.5]
```

**Prompt Enhancement**:
```python
def enhance_music_prompt(user_prompt: str, style: str = None) -> str:
    """
    Enhance user prompt with musical terminology and structure
    """
    enhancements = []
    
    # Add style if specified
    if style:
        enhancements.append(f"{style} style")
    
    # Add production quality indicators
    enhancements.append("high quality")
    enhancements.append("professional production")
    
    # Structure the prompt
    enhanced = f"{user_prompt}, {', '.join(enhancements)}"
    
    return enhanced
```

### Audio-to-MIDI Agent

**Purpose**: Transcribe audio to MIDI notation

**Configuration**:
```yaml
agent:
  name: "audio_to_midi_agent"
  model: "basic_pitch"
  
  capabilities:
    - onset_detection
    - pitch_detection
    - duration_estimation
    - midi_generation
  
  parameters:
    onset_threshold: 0.5
    frame_threshold: 0.3
    minimum_note_length: 0.127  # seconds
    minimum_frequency: 32.7  # Hz (C1)
    maximum_frequency: 2093.0  # Hz (C7)
```

**Processing Pipeline**:
```python
class AudioToMIDIAgent:
    def __init__(self, model_path: str):
        self.model = load_model(model_path)
    
    def process(self, audio_path: str) -> dict:
        """
        Process audio file and generate MIDI
        
        Returns:
            dict: {
                'midi_path': str,
                'confidence': float,
                'metadata': dict
            }
        """
        # 1. Load and preprocess audio
        audio = self.load_audio(audio_path)
        
        # 2. Run inference
        model_output = self.model.predict(audio)
        
        # 3. Post-process predictions
        notes = self.post_process(model_output)
        
        # 4. Generate MIDI
        midi_path = self.generate_midi(notes)
        
        # 5. Calculate confidence
        confidence = self.calculate_confidence(notes)
        
        return {
            'midi_path': midi_path,
            'confidence': confidence,
            'metadata': self.extract_metadata(notes)
        }
```

---

## 🎓 Phin-Specific Agents

### Phin Feature Extraction Agent

**Purpose**: Extract features specific to Thai Phin music

**Configuration**:
```yaml
agent:
  name: "phin_feature_agent"
  music_system: "thai_7_tone"
  
  features:
    - mel_spectrogram
    - cqt_7_bins_per_octave
    - chroma_7_tone
    - onset_strength
    - spectral_features
  
  parameters:
    sample_rate: 22050
    n_fft: 2048
    hop_length: 512
    bins_per_octave: 7  # Thai music uses 7-tone system
```

**Implementation**:
```python
class PhinFeatureAgent:
    def __init__(self, sr=22050):
        self.sr = sr
        self.bins_per_octave = 7  # Thai 7-tone system
    
    def extract_features(self, audio_path: str) -> dict:
        """
        Extract all features for Phin audio
        """
        y, sr = librosa.load(audio_path, sr=self.sr)
        
        features = {
            'mel': self._extract_mel(y),
            'cqt': self._extract_cqt_7tone(y),
            'chroma': self._extract_chroma_7tone(y),
            'onset': self._extract_onset(y),
            'spectral': self._extract_spectral(y)
        }
        
        return features
    
    def _extract_cqt_7tone(self, y):
        """CQT with 7 bins per octave for Thai scale"""
        cqt = librosa.cqt(
            y=y,
            sr=self.sr,
            bins_per_octave=self.bins_per_octave,
            n_bins=self.bins_per_octave * 6  # 6 octaves
        )
        return librosa.amplitude_to_db(np.abs(cqt))
```

### Phin Transcription Agent

**Purpose**: Specialized transcription for Phin music

**Configuration**:
```yaml
agent:
  name: "phin_transcription_agent"
  method: "ewma"  # Energy-based Windowed Moving Average
  
  parameters:
    ewma_alpha: 0.8
    onset_threshold: 0.3
    pitch_range: [100, 2000]  # Hz
    duration_estimation: "onset_diff"
  
  performance_targets:
    onset_f1: 0.95
    pitch_f1: 0.90
    note_f1: 0.85
```

---

## 🔧 Agent Orchestration

### Multi-Agent Workflow

```python
class AgentOrchestrator:
    """
    Orchestrate multiple agents for complex tasks
    """
    
    def __init__(self):
        self.agents = {
            'image_to_music': ImageToMusicAgent(),
            'text_to_music': TextToMusicAgent(),
            'audio_to_midi': AudioToMIDIAgent(),
            'phin_features': PhinFeatureAgent(),
            'phin_transcription': PhinTranscriptionAgent()
        }
    
    def process_image_to_music(self, image_path: str, 
                               user_prompt: str = None,
                               duration: int = 10) -> dict:
        """
        Complete pipeline: Image -> Description -> Music
        """
        # Step 1: Analyze image
        image_agent = self.agents['image_to_music']
        music_description = image_agent.analyze(
            image_path, 
            user_guidance=user_prompt
        )
        
        # Step 2: Generate music
        music_agent = self.agents['text_to_music']
        music_output = music_agent.generate(
            prompt=music_description,
            duration=duration
        )
        
        return music_output
    
    def process_phin_audio(self, audio_path: str) -> dict:
        """
        Complete pipeline: Phin Audio -> Features -> Transcription
        """
        # Step 1: Extract features
        feature_agent = self.agents['phin_features']
        features = feature_agent.extract_features(audio_path)
        
        # Step 2: Transcribe
        transcription_agent = self.agents['phin_transcription']
        midi_output = transcription_agent.transcribe(
            audio_path,
            features=features
        )
        
        return midi_output
```

---

## 📊 Agent Performance Monitoring

### Metrics Collection

```python
class AgentMetrics:
    """
    Collect and analyze agent performance metrics
    """
    
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def log_generation(self, agent_name: str, 
                      duration: float,
                      success: bool,
                      quality_score: float = None):
        """Log generation metrics"""
        self.metrics[agent_name].append({
            'timestamp': datetime.now(),
            'duration': duration,
            'success': success,
            'quality_score': quality_score
        })
    
    def get_statistics(self, agent_name: str) -> dict:
        """Get agent statistics"""
        data = self.metrics[agent_name]
        
        return {
            'total_requests': len(data),
            'success_rate': sum(d['success'] for d in data) / len(data),
            'avg_duration': np.mean([d['duration'] for d in data]),
            'avg_quality': np.mean([d['quality_score'] for d in data 
                                   if d['quality_score'] is not None])
        }
```

---

## 🛡️ Safety & Ethics

### Content Filtering

```python
class SafetyAgent:
    """
    Ensure generated content is safe and appropriate
    """
    
    def __init__(self):
        self.filters = [
            'violence',
            'hate_speech',
            'explicit_content',
            'copyright_infringement'
        ]
    
    def validate_prompt(self, prompt: str) -> tuple[bool, str]:
        """
        Validate user prompt for safety
        
        Returns:
            (is_safe, reason)
        """
        # Check against filters
        for filter_type in self.filters:
            if self._check_filter(prompt, filter_type):
                return False, f"Prompt violates {filter_type} policy"
        
        return True, "Prompt is safe"
    
    def validate_output(self, output_path: str) -> tuple[bool, str]:
        """
        Validate generated content
        """
        # Implement output validation
        return True, "Output is safe"
```

---

## 🎯 Agent Optimization

### Performance Tuning

1. **Batch Processing**:
   - Process multiple requests in parallel
   - Use GPU acceleration when available
   - Implement caching for common requests

2. **Model Optimization**:
   - Use quantized models for faster inference
   - Implement model pruning for efficiency
   - Cache embeddings and intermediate results

3. **Resource Management**:
   - Monitor memory usage
   - Implement graceful degradation
   - Use async processing for I/O operations

---

## 📝 Agent Configuration Files

Save agent configurations in `mcp.json` for easy management and version control.

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Maintainer**: Phin Isan AI Team
