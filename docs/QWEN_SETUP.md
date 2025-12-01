
# Qwen Coder Integration Guide

## Overview

Mozart's Touch now supports Qwen Coder for intelligent prompt conversion, transforming image descriptions into detailed music generation prompts.

## Setup Options

### Option 1: Local Deployment with Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Qwen Coder model
ollama pull qwen2.5-coder:32b

# Start Ollama server (runs on http://localhost:11434)
ollama serve
```

Update `mcp.json`:
```json
{
  "prompt_converter": {
    "type": "llm",
    "model": "qwen2.5-coder:32b",
    "api_base": "http://localhost:11434/v1"
  }
}
```

### Option 2: Remote API Deployment

If you have Qwen Coder deployed on a remote server:

```bash
# Set environment variable
export QWEN_API_BASE=https://your-qwen-server.com/v1
export QWEN_API_KEY=your-api-key
```

Update `mcp.json`:
```json
{
  "prompt_converter": {
    "type": "llm",
    "model": "qwen2.5-coder-32b-instruct",
    "api_base": "https://your-qwen-server.com/v1"
  }
}
```

### Option 3: HuggingFace Inference API

```bash
export QWEN_API_KEY=hf_your_token_here
```

Update `mcp.json`:
```json
{
  "prompt_converter": {
    "type": "llm",
    "model": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "api_base": "https://api-inference.huggingface.co/models"
  }
}
```

## Testing

```bash
# Test with an image
python main.py --image test.jpg --output test_music.wav

# Verify Qwen integration
python -c "
from music_generator import MusicOrchestrator
orch = MusicOrchestrator()
result = orch._convert_description_to_music_prompt('A sunset over mountains')
print(f'Converted prompt: {result}')
"
```

## Model Variants

- **qwen2.5-coder:7b** - Fastest, lowest resource usage
- **qwen2.5-coder:14b** - Balanced performance
- **qwen2.5-coder:32b** - Best quality, highest resource usage

## Performance Tips

1. **GPU Acceleration**: Ensure CUDA is available for faster inference
2. **Batch Processing**: Process multiple prompts together
3. **Caching**: Enable response caching for repeated prompts
4. **Timeout Settings**: Adjust timeout for slower connections

## Troubleshooting

### Connection Issues
```bash
# Test API connectivity
curl http://localhost:11434/v1/models
```

### Model Loading Errors
```bash
# Check Ollama status
ollama list

# Reinstall model if needed
ollama rm qwen2.5-coder:32b
ollama pull qwen2.5-coder:32b
```

### Memory Issues
- Use smaller model variants (7B instead of 32B)
- Enable quantization for reduced memory usage
- Close other applications to free RAM/VRAM
