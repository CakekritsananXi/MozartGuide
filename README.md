# 🎵 Phin Isan AI - Music Generation Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**AI-powered music generation platform for Thai Phin (พิณอีสาน) and general music creation.**

## 🌟 Features

- **Image-to-Music**: Generate music from static images using vision-language models
- **Video-to-Music**: Create synchronized soundtracks for video content
- **Audio-to-MIDI**: Transcribe Phin audio recordings to MIDI format
- **Multi-Agent Architecture**: Modular design with specialized AI agents
- **Agent Router Integration**: Optional routing and orchestration via Agent Router AI
- **REST API**: FastAPI-based web service for remote access
- **Interactive UI**: Streamlit web interface for easy usage

## 🚀 Quick Start

### Installation

1. **Clone the repository** (or open in Replit):
```bash
git clone <your-repo-url>
cd phin-isan-ai
```

2. **Run the setup script**:
```bash
chmod +x setup.sh
./setup.sh
```

Or install manually:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Usage

**Command Line Interface**:
```bash
# Generate music from an image
python main.py --image path/to/image.jpg --output music.wav

# With custom duration and guidance
python main.py --image photo.jpg --duration 20 --guidance 4.0

# Use Agent Router for orchestration
python main.py --image photo.jpg --use-agent-router

# Generate from text prompt
python main.py --prompt "Calm ambient music with soft piano" --output ambient.wav

# Transcribe audio to MIDI
python main.py --audio song.wav --midi-output notes.mid
```

**Web Interface**:
```bash
streamlit run app.py --server.port 5000
```

Then open your browser to the displayed URL.

## 📖 Usage

### Configuration Wizard

On first run, use the Configuration Wizard to set up your models:

1. Select your preferred music generation model (MusicGen, AudioCraft, etc.)
2. Configure model parameters (guidance scale, duration limits, etc.)
3. Set up API keys if using cloud services
4. Save configuration

### Generate Music

#### From Image
1. Navigate to "Image to Music" tab
2. Upload an image (PNG, JPG, JPEG)
3. Optionally add a text prompt for guidance
4. Set duration and other parameters
5. Click "Generate Music"

#### From Text
1. Navigate to "Text to Music" tab
2. Enter your music description
3. Adjust parameters (duration, guidance scale, temperature)
4. Click "Generate Music"

#### From Audio
1. Navigate to "Audio to MIDI" tab
2. Upload an audio file (WAV, MP3, FLAC)
3. Select transcription model
4. Click "Convert to MIDI"

## 🎓 Phin Dataset

This project includes comprehensive resources for Thai Phin music:

### Dataset Structure

```
phin_ai_dataset/
├── audio_sources/          # Raw audio from YouTube
│   ├── lai_mahoree/
│   ├── lai_nok_sai/
│   └── ...
├── processed_audio/        # Preprocessed audio
│   ├── train/
│   ├── val/
│   └── test/
├── sheet_music/           # Musical notation
│   ├── traditional_notation/
│   └── midi_files/
├── research_papers/       # Academic references
└── documentation/         # Guides and tutorials
```

### Lai Phin (ลายพิณ) Patterns

Priority patterns to collect:

- ✅ **ลายมโหรีอีสาน** (Lai Mahoree Isan)
- ⏳ **ลายนกไส่บินข้ามทุ่ง** (Nok Sai)
- ⏳ **ลายแมลงภู่ตอมดอกไม้** (Maleng Phu)
- ⏳ **ลายเต้ยโขง** (Toei Khong)
- ⏳ **ลายเซิ้งบั้งไฟ** (Soeng Bang Fai)

### Data Collection

Download YouTube videos:
```bash
yt-dlp -f bestaudio --extract-audio --audio-format wav \
  -o "audio_sources/%(title)s.%(ext)s" \
  <YOUTUBE_URL>
```

Process audio:
```python
from audio_preprocessing import AudioPreprocessor

preprocessor = AudioPreprocessor(sr=22050)
preprocessor.process_file("input.wav", "output_dir")
```

## 🛠️ Architecture

### Technology Stack

- **Backend**: Python 3.11
- **Web Framework**: Streamlit
- **ML/Audio**:
  - TensorFlow / PyTorch
  - Librosa
  - Basic Pitch (Spotify)
  - Pretty MIDI
- **APIs**: 
  - OpenAI (GPT-4 Vision)
  - Anthropic (Claude)
  - Google (Gemini)

### Models Supported

1. **MusicGen** - Meta's music generation model
2. **AudioCraft** - Advanced audio synthesis
3. **Basic Pitch** - Audio-to-MIDI transcription
4. **Custom Phin Models** - Specialized for Thai music

## 📊 Project Status

### Phase 1: Data Collection (In Progress - 5%)
- ✅ Project structure setup
- ✅ Documentation complete
- ⏳ Video collection (1/130 videos)
- ⏳ MIDI ground truth collection

### Phase 2: Preprocessing (Not Started)
- Audio cleaning
- Segmentation
- Feature extraction

### Phase 3: Model Development (Not Started)
- Transfer learning
- Custom architecture
- Training pipeline

### Phase 4: Evaluation (Not Started)
- Metrics calculation
- Benchmark comparison

### Phase 5: Deployment (Not Started)
- Web application
- Mobile app
- API services

## 🎯 Target Metrics

- **Onset Detection F1**: > 95%
- **Pitch Detection F1**: > 90%
- **Note-level Accuracy**: > 85%

## 🔗 Resources

### Documentation
- [Quick Start Guide](attached_assets/quick_start_guide_1764566914736.md)
- [Master Guide](attached_assets/phin_dataset_master_guide_1764566914735.md)
- [Training Pipeline](attached_assets/training_pipeline_1764566914738.md)
- [YouTube Sources](attached_assets/youtube_sources_1764566914738.md)
- [References](attached_assets/REFERENCES_1764566914737.md)

### Research Papers
- [KMUTT Thai Xylophone Transcription](https://inc.kmutt.ac.th/download/capstone_design_projects/2567/10.pdf)
- [Google Magenta Transcultural ML](https://magenta.withgoogle.com/transcultural)

### Open Source Projects
- [Spotify Basic Pitch](https://github.com/spotify/basic-pitch)
- [Omnizart](https://github.com/Music-and-Culture-Technology-Lab/omnizart)
- [Mozart's Touch](https://github.com/tiffanyblews/mozartstouch)

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add Phin Videos**: Share YouTube links of quality Phin performances
2. **Sheet Music**: Contribute MIDI files or traditional notation
3. **Code**: Improve preprocessing, models, or evaluation
4. **Documentation**: Write tutorials or translate content

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Thai Phin teachers sharing knowledge on YouTube
- KMUTT and Google Magenta research teams
- Open source communities (Spotify, Librosa, etc.)
- Traditional Thai music preservation efforts

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

**สร้างด้วย ❤️ เพื่อการอนุรักษ์และพัฒนาดนตรีไทย**

**Created with ❤️ for Thai Music Preservation and Development**

*Last Updated: December 2024*
*Version: 1.0.0*