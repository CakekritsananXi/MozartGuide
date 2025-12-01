import streamlit as st
import json
import importlib
import importlib.util
import sys
import time
from typing import Dict, Any, Tuple

st.set_page_config(
    page_title="Mozart's Touch - Interactive Guide",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --primary-color: #6366F1;
    --secondary-color: #8B5CF6;
    --accent-color: #A78BFA;
    --bg-dark: #1E1E2E;
    --bg-card: #2D2D3F;
    --text-primary: #E2E8F0;
    --text-secondary: #94A3B8;
    --border-color: #3D3D5C;
    --success-color: #10B981;
    --warning-color: #F59E0B;
    --error-color: #EF4444;
}

.stApp {
    background: linear-gradient(135deg, #0F0F1A 0%, #1A1A2E 50%, #16213E 100%);
}

.main-header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.sub-header {
    color: var(--text-secondary);
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

.section-title {
    color: var(--primary-color);
    font-size: 1.5rem;
    font-weight: 600;
    border-left: 4px solid var(--secondary-color);
    padding-left: 1rem;
    margin: 2rem 0 1rem 0;
}

.code-block {
    background: var(--bg-dark);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875rem;
    overflow-x: auto;
    position: relative;
}

.info-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.step-indicator {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border-radius: 50%;
    font-weight: 600;
    margin-right: 0.75rem;
}

.status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
}

.status-success {
    background: rgba(16, 185, 129, 0.2);
    color: var(--success-color);
}

.status-warning {
    background: rgba(245, 158, 11, 0.2);
    color: var(--warning-color);
}

.status-error {
    background: rgba(239, 68, 68, 0.2);
    color: var(--error-color);
}

div[data-testid="stExpander"] {
    background: rgba(45, 45, 63, 0.5);
    border: 1px solid var(--border-color);
    border-radius: 12px;
}

div[data-testid="stExpander"] summary {
    font-weight: 600;
    color: var(--text-primary);
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    transition: all 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    border-radius: 8px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: var(--bg-card);
    border-radius: 8px;
    color: var(--text-secondary);
    border: 1px solid var(--border-color);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
}

pre {
    background: #1a1a2e !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

code {
    font-family: 'JetBrains Mono', monospace !important;
    color: #A78BFA !important;
}

.stMarkdown a {
    color: var(--primary-color);
    text-decoration: none;
}

.stMarkdown a:hover {
    color: var(--secondary-color);
    text-decoration: underline;
}

h1, h2, h3 {
    color: var(--text-primary) !important;
}

p, li {
    color: var(--text-secondary);
}

.copy-code-container {
    position: relative;
    margin: 1rem 0;
}

.copy-btn-overlay {
    position: absolute;
    top: 8px;
    right: 8px;
    z-index: 100;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_code_with_copy(code: str, language: str = "python", key: str = "default"):
    """Render a code block with functional copy-to-clipboard button using Streamlit components"""
    st.code(code, language=language)
    
    escaped_code = code.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${").replace("'", "\\'").replace("\n", "\\n")
    
    copy_html = f'''
    <div id="copy-container-{key}" style="margin-top: -10px; margin-bottom: 10px;">
        <button id="copy-btn-{key}" onclick="
            navigator.clipboard.writeText('{escaped_code}'.replace(/\\\\n/g, '\\n')).then(function() {{
                document.getElementById('copy-btn-{key}').innerHTML = '✅ Copied!';
                document.getElementById('copy-btn-{key}').style.background = 'linear-gradient(135deg, #10B981, #059669)';
                setTimeout(function() {{
                    document.getElementById('copy-btn-{key}').innerHTML = '📋 Copy Code';
                    document.getElementById('copy-btn-{key}').style.background = 'linear-gradient(135deg, #6366F1, #8B5CF6)';
                }}, 2000);
            }}).catch(function(err) {{
                document.getElementById('copy-btn-{key}').innerHTML = '❌ Failed';
                console.error('Copy failed:', err);
            }});
        " style="
            background: linear-gradient(135deg, #6366F1, #8B5CF6);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 500;
            font-family: inherit;
            transition: all 0.2s;
        " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 12px rgba(99, 102, 241, 0.4)';"
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
            📋 Copy Code
        </button>
    </div>
    '''
    
    import streamlit.components.v1 as components
    components.html(copy_html, height=50)

def check_package_installed(package_name: str) -> Tuple[bool, str]:
    """Check if a package is installed and return its version using robust methods"""
    
    def get_version_from_metadata(pkg_name: str) -> str:
        """Try to get version from package metadata"""
        try:
            from importlib.metadata import version as get_pkg_version
            return get_pkg_version(pkg_name)
        except:
            return None
    
    package_configs = {
        "PIL": {"import": "PIL", "pip_name": "Pillow", "version_attr": "__version__"},
        "cv2": {"import": "cv2", "pip_name": "opencv-python", "version_attr": "__version__"},
        "torch": {"import": "torch", "pip_name": "torch", "version_attr": "__version__"},
        "transformers": {"import": "transformers", "pip_name": "transformers", "version_attr": "__version__"},
        "accelerate": {"import": "accelerate", "pip_name": "accelerate", "version_attr": "__version__"},
        "audiocraft": {"import": "audiocraft", "pip_name": "audiocraft", "version_attr": "__version__"},
        "scipy": {"import": "scipy", "pip_name": "scipy", "version_attr": "__version__"},
        "soundfile": {"import": "soundfile", "pip_name": "soundfile", "version_attr": "__version__"},
        "moviepy": {"import": "moviepy", "pip_name": "moviepy", "version_attr": "__version__"},
        "fastapi": {"import": "fastapi", "pip_name": "fastapi", "version_attr": "__version__"},
        "uvicorn": {"import": "uvicorn", "pip_name": "uvicorn", "version_attr": "__version__"},
        "openai": {"import": "openai", "pip_name": "openai", "version_attr": "__version__"},
    }
    
    config = package_configs.get(package_name, {
        "import": package_name, 
        "pip_name": package_name, 
        "version_attr": "__version__"
    })
    
    import_name = config["import"]
    pip_name = config["pip_name"]
    version_attr = config["version_attr"]
    
    spec = importlib.util.find_spec(import_name)
    if spec is None:
        return False, "Not installed"
    
    version = get_version_from_metadata(pip_name)
    if version:
        return True, version
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, version_attr, None)
        if version:
            return True, str(version)
    except Exception:
        pass
    
    return True, "✓ Found"

def get_default_config() -> Dict[str, Any]:
    """Returns the default Mozart's Touch configuration"""
    return {
        "music_generator": {
            "type": "musicgen",
            "model_name": "facebook/musicgen-small",
            "duration": 10,
            "guidance_scale": 3.0,
            "temperature": 1.0
        },
        "captioner": {
            "type": "blip2",
            "model_name": "Salesforce/blip2-opt-2.7b",
            "device": "cuda"
        },
        "prompt_converter": {
            "type": "llm",
            "model": "gpt-3.5-turbo",
            "system_prompt": "Convert the following image description into a music generation prompt..."
        },
        "video_processor": {
            "fps_sample_rate": 1,
            "max_frames": 30,
            "resize_width": 512,
            "resize_height": 512
        },
        "output": {
            "format": "wav",
            "sample_rate": 32000,
            "save_intermediate": True
        },
        "test_mode": False
    }

def sidebar_navigation():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <span style="font-size: 3rem;">🎵</span>
            <h2 style="margin: 0.5rem 0; background: linear-gradient(135deg, #6366F1, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Mozart's Touch</h2>
            <p style="color: #94A3B8; font-size: 0.875rem;">Interactive Tutorial Guide</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        sections = {
            "🏠 Overview": "overview",
            "📋 Prerequisites": "prerequisites",
            "⚙️ Configuration Wizard": "config",
            "📦 Dependencies": "dependencies",
            "🔧 Installation": "installation",
            "💻 CLI Usage": "cli",
            "🌐 Web API": "api",
            "🎯 Examples": "examples",
            "❓ Troubleshooting": "troubleshooting"
        }
        
        if "current_section" not in st.session_state:
            st.session_state.current_section = "overview"
        
        for label, key in sections.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.current_section = key
        
        st.divider()
        
        st.markdown("""
        <div style="padding: 1rem; background: rgba(99, 102, 241, 0.1); border-radius: 8px; margin-top: 1rem;">
            <p style="color: #94A3B8; font-size: 0.75rem; margin: 0;">
                <strong style="color: #A78BFA;">Version:</strong> 1.0.0<br>
                <strong style="color: #A78BFA;">Framework:</strong> Mozart's Touch<br>
                <strong style="color: #A78BFA;">License:</strong> MIT
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_overview():
    """Render the overview section"""
    st.markdown('<h1 class="main-header">Mozart\'s Touch</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered music generation from images and videos</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2)); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #3D3D5C;">
            <span style="font-size: 2rem;">🖼️</span>
            <h3 style="margin: 0.5rem 0; color: #E2E8F0;">Image to Music</h3>
            <p style="color: #94A3B8; font-size: 0.875rem; margin: 0;">Generate music from static images</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2)); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #3D3D5C;">
            <span style="font-size: 2rem;">🎬</span>
            <h3 style="margin: 0.5rem 0; color: #E2E8F0;">Video to Music</h3>
            <p style="color: #94A3B8; font-size: 0.875rem; margin: 0;">Create soundtracks for videos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2)); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #3D3D5C;">
            <span style="font-size: 2rem;">🤖</span>
            <h3 style="margin: 0.5rem 0; color: #E2E8F0;">AI-Powered</h3>
            <p style="color: #94A3B8; font-size: 0.875rem; margin: 0;">BLIP2 + MusicGen pipeline</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2)); padding: 1.5rem; border-radius: 12px; text-align: center; border: 1px solid #3D3D5C;">
            <span style="font-size: 2rem;">🌐</span>
            <h3 style="margin: 0.5rem 0; color: #E2E8F0;">REST API</h3>
            <p style="color: #94A3B8; font-size: 0.875rem; margin: 0;">FastAPI web interface</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 How It Works")
    
    st.markdown("""
    <div style="background: #1E1E2E; padding: 2rem; border-radius: 12px; border: 1px solid #3D3D5C;">
        <div style="display: flex; align-items: center; justify-content: space-around; flex-wrap: wrap; gap: 1rem;">
            <div style="text-align: center;">
                <div style="font-size: 2.5rem;">🖼️</div>
                <p style="color: #94A3B8; margin: 0.5rem 0 0 0;">Image/Video</p>
            </div>
            <div style="color: #6366F1; font-size: 1.5rem;">→</div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem;">👁️</div>
                <p style="color: #94A3B8; margin: 0.5rem 0 0 0;">BLIP2 Captioner</p>
            </div>
            <div style="color: #6366F1; font-size: 1.5rem;">→</div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem;">🧠</div>
                <p style="color: #94A3B8; margin: 0.5rem 0 0 0;">LLM Converter</p>
            </div>
            <div style="color: #6366F1; font-size: 1.5rem;">→</div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem;">🎵</div>
                <p style="color: #94A3B8; margin: 0.5rem 0 0 0;">MusicGen</p>
            </div>
            <div style="color: #6366F1; font-size: 1.5rem;">→</div>
            <div style="text-align: center;">
                <div style="font-size: 2.5rem;">🔊</div>
                <p style="color: #94A3B8; margin: 0.5rem 0 0 0;">Audio Output</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📚 Quick Start")
    
    with st.expander("🚀 5-Minute Setup Guide", expanded=True):
        st.markdown("""
        1. **Clone the repository**
        2. **Install dependencies** with pip or conda
        3. **Configure** your `config.yaml` file
        4. **Download** the pre-trained models
        5. **Run** via CLI or Web API
        """)
        
        quick_start_code = """# Quick start commands
git clone https://github.com/your-repo/mozarts-touch.git
cd mozarts-touch
pip install -r requirements.txt
python main.py --image path/to/image.jpg --output music.wav"""
        
        render_code_with_copy(quick_start_code, "bash", "quickstart")

def render_prerequisites():
    """Render prerequisites section"""
    st.markdown("## 📋 Prerequisites")
    st.markdown("Ensure your system meets the following requirements before installation.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💻 System Requirements")
        
        requirements = [
            ("Python", "3.8+", True),
            ("CUDA", "11.7+ (recommended)", None),
            ("RAM", "16GB minimum", None),
            ("VRAM", "8GB+ for GPU inference", None),
            ("Disk Space", "10GB+ for models", None)
        ]
        
        for name, version, status in requirements:
            icon = "✅" if status else "⚠️" if status is None else "❌"
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 0.5rem; background: rgba(45, 45, 63, 0.5); border-radius: 8px; margin: 0.5rem 0;">
                <span style="margin-right: 0.5rem;">{icon}</span>
                <span style="color: #E2E8F0; flex: 1;">{name}</span>
                <span style="color: #94A3B8;">{version}</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔑 API Keys Required")
        
        api_keys = [
            ("OpenAI API Key", "For LLM prompt conversion", "OPENAI_API_KEY"),
            ("Hugging Face Token", "For model downloads", "HF_TOKEN"),
        ]
        
        for name, desc, env_var in api_keys:
            st.markdown(f"""
            <div style="padding: 1rem; background: rgba(45, 45, 63, 0.5); border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #6366F1;">
                <strong style="color: #E2E8F0;">{name}</strong>
                <p style="color: #94A3B8; font-size: 0.875rem; margin: 0.25rem 0 0 0;">{desc}</p>
                <code style="font-size: 0.75rem;">{env_var}</code>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 🐍 Python Dependencies")
    
    with st.expander("View Required Packages"):
        dependencies_code = """# Core Dependencies
torch>=2.0.0
transformers>=4.30.0
accelerate>=0.20.0
diffusers>=0.18.0

# Audio Processing
audiocraft>=1.0.0
scipy>=1.10.0
soundfile>=0.12.0

# Image/Video Processing
Pillow>=9.0.0
opencv-python>=4.7.0
moviepy>=1.0.0

# Web API
fastapi>=0.100.0
uvicorn>=0.22.0
python-multipart>=0.0.6

# LLM Integration
openai>=1.0.0

# Utilities
pyyaml>=6.0
tqdm>=4.65.0
numpy>=1.24.0"""
        
        render_code_with_copy(dependencies_code, "text", "prereq_deps")

def render_config_wizard():
    """Render interactive configuration wizard"""
    st.markdown("## ⚙️ Configuration Wizard")
    st.markdown("Use this interactive wizard to generate your `config.yaml` file.")
    
    if "config" not in st.session_state:
        st.session_state.config = get_default_config()
    
    config = st.session_state.config
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎵 Music Generator",
        "👁️ Captioner", 
        "🧠 Prompt Converter",
        "🎬 Video Processor",
        "📤 Output Settings"
    ])
    
    with tab1:
        st.markdown("### Music Generator Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            generator_type = st.selectbox(
                "Generator Type",
                ["musicgen", "suno"],
                index=0 if config["music_generator"]["type"] == "musicgen" else 1,
                help="Choose the music generation backend"
            )
            config["music_generator"]["type"] = generator_type
            
            if generator_type == "musicgen":
                model_options = [
                    "facebook/musicgen-small",
                    "facebook/musicgen-medium", 
                    "facebook/musicgen-large",
                    "facebook/musicgen-melody"
                ]
                model_name = st.selectbox(
                    "Model",
                    model_options,
                    index=model_options.index(config["music_generator"]["model_name"]) if config["music_generator"]["model_name"] in model_options else 0,
                    help="Larger models produce better quality but require more VRAM"
                )
                config["music_generator"]["model_name"] = model_name
        
        with col2:
            duration = st.slider(
                "Duration (seconds)",
                min_value=5,
                max_value=60,
                value=config["music_generator"]["duration"],
                help="Length of generated audio"
            )
            config["music_generator"]["duration"] = duration
            
            guidance_scale = st.slider(
                "Guidance Scale",
                min_value=1.0,
                max_value=10.0,
                value=float(config["music_generator"]["guidance_scale"]),
                step=0.5,
                help="Higher values follow the prompt more closely"
            )
            config["music_generator"]["guidance_scale"] = guidance_scale
            
            temperature = st.slider(
                "Temperature",
                min_value=0.1,
                max_value=2.0,
                value=float(config["music_generator"]["temperature"]),
                step=0.1,
                help="Higher values produce more creative/random outputs"
            )
            config["music_generator"]["temperature"] = temperature
    
    with tab2:
        st.markdown("### Image Captioner Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            captioner_type = st.selectbox(
                "Captioner Type",
                ["blip2", "llava", "custom"],
                index=0,
                help="Vision-language model for image understanding"
            )
            config["captioner"]["type"] = captioner_type
            
            if captioner_type == "blip2":
                blip_models = [
                    "Salesforce/blip2-opt-2.7b",
                    "Salesforce/blip2-opt-6.7b",
                    "Salesforce/blip2-flan-t5-xl"
                ]
                blip_model = st.selectbox(
                    "BLIP2 Model",
                    blip_models,
                    index=0,
                    help="Choose based on your available VRAM"
                )
                config["captioner"]["model_name"] = blip_model
        
        with col2:
            device = st.selectbox(
                "Device",
                ["cuda", "cpu", "mps"],
                index=0,
                help="Processing device (cuda recommended for speed)"
            )
            config["captioner"]["device"] = device
    
    with tab3:
        st.markdown("### Prompt Converter Configuration")
        
        converter_type = st.selectbox(
            "Converter Type",
            ["llm", "template", "direct"],
            index=0,
            help="Method for converting image descriptions to music prompts"
        )
        config["prompt_converter"]["type"] = converter_type
        
        if converter_type == "llm":
            col1, col2 = st.columns(2)
            
            with col1:
                llm_model = st.selectbox(
                    "LLM Model",
                    ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "claude-3-sonnet"],
                    index=0,
                    help="LLM for creative prompt generation"
                )
                config["prompt_converter"]["model"] = llm_model
            
            with col2:
                st.markdown("**System Prompt Preview:**")
                system_prompt = st.text_area(
                    "System Prompt",
                    value="""Convert the following image description into a detailed music generation prompt. Focus on:
- Mood and atmosphere
- Tempo and rhythm
- Instrumentation suggestions
- Musical genre that fits the scene""",
                    height=150,
                    label_visibility="collapsed"
                )
                config["prompt_converter"]["system_prompt"] = system_prompt
    
    with tab4:
        st.markdown("### Video Processing Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fps_sample = st.number_input(
                "FPS Sample Rate",
                min_value=0.1,
                max_value=30.0,
                value=float(config["video_processor"]["fps_sample_rate"]),
                step=0.5,
                help="Frames per second to sample from video"
            )
            config["video_processor"]["fps_sample_rate"] = fps_sample
            
            max_frames = st.number_input(
                "Max Frames",
                min_value=1,
                max_value=100,
                value=config["video_processor"]["max_frames"],
                help="Maximum frames to process"
            )
            config["video_processor"]["max_frames"] = max_frames
        
        with col2:
            resize_width = st.number_input(
                "Resize Width",
                min_value=128,
                max_value=1024,
                value=config["video_processor"]["resize_width"],
                step=64,
                help="Width for frame resizing"
            )
            config["video_processor"]["resize_width"] = resize_width
            
            resize_height = st.number_input(
                "Resize Height",
                min_value=128,
                max_value=1024,
                value=config["video_processor"]["resize_height"],
                step=64,
                help="Height for frame resizing"
            )
            config["video_processor"]["resize_height"] = resize_height
    
    with tab5:
        st.markdown("### Output Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            output_format = st.selectbox(
                "Output Format",
                ["wav", "mp3", "flac", "ogg"],
                index=0,
                help="Audio output format"
            )
            config["output"]["format"] = output_format
            
            sample_rate = st.selectbox(
                "Sample Rate",
                [16000, 22050, 32000, 44100, 48000],
                index=2,
                help="Audio sample rate in Hz"
            )
            config["output"]["sample_rate"] = sample_rate
        
        with col2:
            save_intermediate = st.checkbox(
                "Save Intermediate Results",
                value=config["output"]["save_intermediate"],
                help="Save captions and prompts alongside audio"
            )
            config["output"]["save_intermediate"] = save_intermediate
            
            test_mode = st.checkbox(
                "Test Mode",
                value=config["test_mode"],
                help="Run without loading large models (for testing)"
            )
            config["test_mode"] = test_mode
    
    st.markdown("---")
    st.markdown("### 📄 Generated Configuration")
    
    import yaml
    yaml_output = yaml.dump(config, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    render_code_with_copy(yaml_output, "yaml", "config_yaml")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col2:
        st.download_button(
            "💾 Download config.yaml",
            yaml_output,
            file_name="config.yaml",
            mime="text/yaml",
            use_container_width=True
        )
    
    with col3:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.session_state.config = get_default_config()
            st.rerun()

def render_dependencies():
    """Render dependency checker section with real package verification"""
    st.markdown("## 📦 Dependency Checker")
    st.markdown("Verify your environment has all required packages installed.")
    
    dependencies = {
        "Core": [
            ("torch", "Deep learning framework", "2.0.0+"),
            ("transformers", "Hugging Face models", "4.30.0+"),
            ("accelerate", "Model acceleration", "0.20.0+"),
        ],
        "Audio": [
            ("audiocraft", "MusicGen models", "1.0.0+"),
            ("scipy", "Audio processing", "1.10.0+"),
            ("soundfile", "Audio I/O", "0.12.0+"),
        ],
        "Vision": [
            ("PIL", "Image processing", "9.0.0+"),
            ("cv2", "OpenCV", "4.7.0+"),
            ("moviepy", "Video processing", "1.0.0+"),
        ],
        "Web API": [
            ("fastapi", "Web framework", "0.100.0+"),
            ("uvicorn", "ASGI server", "0.22.0+"),
        ],
        "LLM": [
            ("openai", "OpenAI API", "1.0.0+"),
        ]
    }
    
    if "check_results" not in st.session_state:
        st.session_state.check_results = {}
    
    col1, col2 = st.columns([1, 3])
    with col1:
        check_btn = st.button("🔍 Check Dependencies", use_container_width=True)
    
    if check_btn:
        with st.spinner("Checking installed packages..."):
            st.session_state.check_results = {}
            progress_bar = st.progress(0)
            
            all_packages = [(pkg, cat) for cat, pkgs in dependencies.items() for pkg, _, _ in pkgs]
            total = len(all_packages)
            
            for idx, (pkg_name, category) in enumerate(all_packages):
                installed, version = check_package_installed(pkg_name)
                if installed:
                    st.session_state.check_results[pkg_name] = ("success", version)
                else:
                    st.session_state.check_results[pkg_name] = ("error", version)
                progress_bar.progress((idx + 1) / total)
                time.sleep(0.1)
            
            progress_bar.empty()
        st.rerun()
    
    installed_count = sum(1 for s, _ in st.session_state.check_results.values() if s == "success")
    total_count = sum(len(pkgs) for pkgs in dependencies.values())
    
    if st.session_state.check_results:
        if installed_count == total_count:
            st.success(f"✅ All {total_count} packages are installed!")
        else:
            st.warning(f"⚠️ {installed_count}/{total_count} packages installed. Missing packages shown below.")
    
    for category, packages in dependencies.items():
        with st.expander(f"📁 {category}", expanded=True):
            for pkg_name, desc, required_ver in packages:
                result = st.session_state.check_results.get(pkg_name, ("pending", "-"))
                status, version = result
                
                if status == "success":
                    icon = "✅"
                    badge_style = "background: rgba(16, 185, 129, 0.2); color: #10B981;"
                elif status == "error":
                    icon = "❌"
                    badge_style = "background: rgba(239, 68, 68, 0.2); color: #EF4444;"
                else:
                    icon = "⏳"
                    badge_style = "background: rgba(245, 158, 11, 0.2); color: #F59E0B;"
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 0.75rem; background: rgba(45, 45, 63, 0.5); border-radius: 8px; margin: 0.5rem 0;">
                    <span style="margin-right: 0.75rem; font-size: 1.25rem;">{icon}</span>
                    <div style="flex: 1;">
                        <strong style="color: #E2E8F0;">{pkg_name}</strong>
                        <p style="color: #94A3B8; font-size: 0.75rem; margin: 0;">{desc}</p>
                    </div>
                    <span style="color: #94A3B8; font-size: 0.875rem; margin-right: 1rem;">Required: {required_ver}</span>
                    <span style="display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 500; {badge_style}">{version}</span>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔧 Installation Commands")
    
    install_tabs = st.tabs(["pip", "conda", "requirements.txt"])
    
    with install_tabs[0]:
        pip_code = """# Install all dependencies with pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers accelerate diffusers
pip install audiocraft scipy soundfile
pip install Pillow opencv-python moviepy
pip install fastapi uvicorn python-multipart
pip install openai pyyaml tqdm"""
        render_code_with_copy(pip_code, "bash", "pip_install")
    
    with install_tabs[1]:
        conda_code = """# Create conda environment
conda create -n mozarts-touch python=3.10 -y
conda activate mozarts-touch

# Install PyTorch with CUDA
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# Install other dependencies
pip install transformers accelerate audiocraft
pip install fastapi uvicorn openai"""
        render_code_with_copy(conda_code, "bash", "conda_install")
    
    with install_tabs[2]:
        req_code = """# requirements.txt
torch>=2.0.0
transformers>=4.30.0
accelerate>=0.20.0
audiocraft>=1.0.0
scipy>=1.10.0
soundfile>=0.12.0
Pillow>=9.0.0
opencv-python>=4.7.0
moviepy>=1.0.0
fastapi>=0.100.0
uvicorn>=0.22.0
openai>=1.0.0
pyyaml>=6.0
tqdm>=4.65.0"""
        render_code_with_copy(req_code, "text", "requirements")

def render_installation():
    """Render installation guide with model download tracking"""
    st.markdown("## 🔧 Installation Guide")
    
    st.markdown("### 📥 Model Downloads")
    st.markdown("Mozart's Touch requires several pre-trained models. Use the tracker below to manage downloads.")
    
    models = [
        {
            "name": "MusicGen Small",
            "id": "facebook/musicgen-small",
            "size": "1.5 GB",
            "description": "Lightweight music generation model",
            "vram": "4 GB"
        },
        {
            "name": "MusicGen Medium",
            "id": "facebook/musicgen-medium",
            "size": "3.3 GB",
            "description": "Balanced quality and performance",
            "vram": "8 GB"
        },
        {
            "name": "MusicGen Large",
            "id": "facebook/musicgen-large",
            "size": "6.9 GB",
            "description": "Highest quality music generation",
            "vram": "16 GB"
        },
        {
            "name": "BLIP2 OPT 2.7B",
            "id": "Salesforce/blip2-opt-2.7b",
            "size": "5.4 GB",
            "description": "Image captioning model",
            "vram": "8 GB"
        },
        {
            "name": "BLIP2 FlanT5-XL",
            "id": "Salesforce/blip2-flan-t5-xl",
            "size": "7.2 GB",
            "description": "Enhanced captioning model",
            "vram": "12 GB"
        }
    ]
    
    from datetime import datetime
    
    if "model_status" not in st.session_state:
        st.session_state.model_status = {}
    
    for m in models:
        if m["id"] not in st.session_state.model_status:
            st.session_state.model_status[m["id"]] = {
                "status": "pending",
                "progress": 0,
                "downloaded_at": None
            }
    
    downloaded_count = sum(1 for s in st.session_state.model_status.values() if s["status"] == "downloaded")
    pending_count = len(models) - downloaded_count
    
    st.markdown(f"""
    <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
        <div style="flex: 1; padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.3);">
            <span style="color: #10B981; font-size: 1.5rem; font-weight: bold;">{downloaded_count}</span>
            <span style="color: #94A3B8;"> / {len(models)} Downloaded</span>
        </div>
        <div style="flex: 1; padding: 1rem; background: rgba(245, 158, 11, 0.1); border-radius: 8px; border: 1px solid rgba(245, 158, 11, 0.3);">
            <span style="color: #F59E0B; font-size: 1.5rem; font-weight: bold;">{pending_count}</span>
            <span style="color: #94A3B8;"> Pending</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_dl_all, col_reset_all = st.columns([1, 1])
    with col_dl_all:
        if st.button("📥 Download All Models", use_container_width=True, help="Simulate downloading all models"):
            for m in models:
                st.session_state.model_status[m["id"]] = {
                    "status": "downloaded",
                    "progress": 100,
                    "downloaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            st.rerun()
    with col_reset_all:
        if st.button("🔄 Reset All Status", use_container_width=True):
            for m in models:
                st.session_state.model_status[m["id"]] = {
                    "status": "pending",
                    "progress": 0,
                    "downloaded_at": None
                }
            st.rerun()
    
    for model in models:
        model_state = st.session_state.model_status[model["id"]]
        status = model_state["status"]
        progress = model_state.get("progress", 0)
        downloaded_at = model_state.get("downloaded_at")
        
        status_icon = "✅" if status == "downloaded" else "⏳" if status == "downloading" else "📥"
        
        with st.expander(f"{status_icon} {model['name']}", expanded=(status == "downloading")):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Model ID:** `{model['id']}`")
                st.markdown(f"**Description:** {model['description']}")
                st.markdown(f"**Size:** {model['size']} | **VRAM Required:** {model['vram']}")
                if downloaded_at:
                    st.caption(f"✅ Completed at: {downloaded_at}")
            
            with col2:
                if status == "pending":
                    if st.button(f"📥 Start Download", key=f"dl_{model['id']}"):
                        st.session_state.model_status[model["id"]] = {
                            "status": "downloading",
                            "progress": 0,
                            "downloaded_at": None
                        }
                        st.rerun()
                        
                elif status == "downloading":
                    st.progress(progress / 100, text=f"Downloading... {progress}%")
                    
                    if st.button("⏭️ Complete", key=f"complete_{model['id']}", help="Skip to completion"):
                        st.session_state.model_status[model["id"]] = {
                            "status": "downloaded",
                            "progress": 100,
                            "downloaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.rerun()
                    
                    if progress < 100:
                        new_progress = min(progress + 20, 100)
                        st.session_state.model_status[model["id"]]["progress"] = new_progress
                        
                        if new_progress >= 100:
                            st.session_state.model_status[model["id"]]["status"] = "downloaded"
                            st.session_state.model_status[model["id"]]["downloaded_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        time.sleep(0.8)
                        st.rerun()
                else:
                    st.success("✅ Ready to use")
                    if st.button("🔄 Reset", key=f"reset_{model['id']}"):
                        st.session_state.model_status[model["id"]] = {
                            "status": "pending",
                            "progress": 0,
                            "downloaded_at": None
                        }
                        st.rerun()
            
            st.markdown("**Download Command:**")
            dl_code = f"""from huggingface_hub import snapshot_download

# Download model
snapshot_download(
    repo_id="{model['id']}", 
    local_dir="./models/{model['id'].split('/')[-1]}"
)"""
            render_code_with_copy(dl_code, "python", f"dl_code_{model['id'].replace('/', '_')}")
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Setup Script")
    
    setup_code = """#!/bin/bash
# setup.sh - Complete Mozart's Touch Setup

# Create project directory
mkdir -p mozarts-touch && cd mozarts-touch

# Clone repository
git clone https://github.com/your-repo/mozarts-touch.git .

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download models (optional - will download on first run)
python -c "from audiocraft.models import MusicGen; MusicGen.get_pretrained('facebook/musicgen-small')"

# Set up environment variables
echo "OPENAI_API_KEY=your-key-here" > .env
echo "HF_TOKEN=your-token-here" >> .env

# Verify installation
python -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"

echo "✅ Setup complete! Run 'python main.py --help' to get started."
"""
    render_code_with_copy(setup_code, "bash", "setup_script")

def render_cli_usage():
    """Render CLI usage examples"""
    st.markdown("## 💻 Command-Line Interface")
    st.markdown("Mozart's Touch provides a powerful CLI for music generation.")
    
    st.markdown("### 📌 Basic Commands")
    
    commands = [
        {
            "title": "Generate from Image",
            "description": "Create music from a single image",
            "command": """python main.py \\
    --image path/to/image.jpg \\
    --output generated_music.wav \\
    --duration 15""",
            "icon": "🖼️"
        },
        {
            "title": "Generate from Video",
            "description": "Create a synchronized soundtrack for a video",
            "command": """python main.py \\
    --video path/to/video.mp4 \\
    --output soundtrack.wav \\
    --sync-length""",
            "icon": "🎬"
        },
        {
            "title": "Batch Processing",
            "description": "Process multiple images in a directory",
            "command": """python main.py \\
    --input-dir ./images \\
    --output-dir ./music \\
    --format mp3 \\
    --parallel 4""",
            "icon": "📁"
        },
        {
            "title": "Custom Configuration",
            "description": "Use a custom configuration file",
            "command": """python main.py \\
    --config custom_config.yaml \\
    --image input.jpg \\
    --verbose""",
            "icon": "⚙️"
        },
        {
            "title": "Test Mode",
            "description": "Run without loading models (for testing)",
            "command": """python main.py \\
    --image test.jpg \\
    --test-mode \\
    --dry-run""",
            "icon": "🧪"
        }
    ]
    
    for cmd in commands:
        with st.expander(f"{cmd['icon']} {cmd['title']}", expanded=False):
            st.markdown(f"_{cmd['description']}_")
            render_code_with_copy(cmd["command"], "bash", f"cmd_{cmd['title'].replace(' ', '_')}")
    
    st.markdown("---")
    st.markdown("### 🎛️ All CLI Options")
    
    options_data = """
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--image` | PATH | - | Path to input image |
| `--video` | PATH | - | Path to input video |
| `--output` | PATH | `output.wav` | Output audio file path |
| `--config` | PATH | `config.yaml` | Configuration file |
| `--duration` | INT | 10 | Audio duration in seconds |
| `--format` | STR | `wav` | Output format (wav/mp3/flac) |
| `--model` | STR | `small` | MusicGen model size |
| `--guidance` | FLOAT | 3.0 | Guidance scale |
| `--temperature` | FLOAT | 1.0 | Generation temperature |
| `--seed` | INT | random | Random seed for reproducibility |
| `--device` | STR | `cuda` | Processing device |
| `--verbose` | FLAG | False | Enable verbose output |
| `--test-mode` | FLAG | False | Run without loading models |
| `--dry-run` | FLAG | False | Show what would be done |
    """
    
    st.markdown(options_data)
    
    st.markdown("---")
    st.markdown("### 📝 Example Workflows")
    
    workflow_tabs = st.tabs(["Single Image", "Video Soundtrack", "Batch Mode", "Advanced"])
    
    with workflow_tabs[0]:
        st.markdown("#### Generate Music from a Single Image")
        single_img_code = """# Step 1: Prepare your image
# Ensure image is in JPG/PNG format, any resolution works

# Step 2: Run generation with default settings
python main.py --image sunset_beach.jpg --output beach_music.wav

# Step 3: With custom parameters
python main.py \\
    --image sunset_beach.jpg \\
    --output beach_music.wav \\
    --duration 30 \\
    --model medium \\
    --guidance 4.0 \\
    --seed 42

# Step 4: Check the output
ffprobe beach_music.wav  # Verify audio properties"""
        render_code_with_copy(single_img_code, "bash", "single_img_workflow")
    
    with workflow_tabs[1]:
        st.markdown("#### Create Video Soundtrack")
        video_code = """# Analyze video and generate matching music
python main.py \\
    --video travel_montage.mp4 \\
    --output soundtrack.wav \\
    --sync-length \\
    --fps-sample 0.5

# Merge audio with video (using ffmpeg)
ffmpeg -i travel_montage.mp4 -i soundtrack.wav \\
    -c:v copy -map 0:v:0 -map 1:a:0 \\
    output_with_music.mp4"""
        render_code_with_copy(video_code, "bash", "video_workflow")
    
    with workflow_tabs[2]:
        st.markdown("#### Batch Process Multiple Images")
        batch_code = """# Process entire directory
python main.py \\
    --input-dir ./vacation_photos \\
    --output-dir ./vacation_music \\
    --format mp3 \\
    --duration 10 \\
    --parallel 4 \\
    --progress

# With specific file pattern
python main.py \\
    --input-dir ./photos \\
    --pattern "*.jpg" \\
    --output-dir ./music \\
    --naming "{original}_music"

# Results will be saved as:
# vacation_photos/beach.jpg -> vacation_music/beach.mp3
# vacation_photos/mountain.jpg -> vacation_music/mountain.mp3"""
        render_code_with_copy(batch_code, "bash", "batch_workflow")
    
    with workflow_tabs[3]:
        st.markdown("#### Advanced Usage")
        advanced_code = """# Use custom prompt template
python main.py \\
    --image scene.jpg \\
    --prompt-template "Create {mood} music with {genre} influences" \\
    --mood calm \\
    --genre ambient

# Chain multiple operations
python main.py \\
    --image input.jpg \\
    --output temp.wav \\
    --save-caption caption.txt \\
    --save-prompt prompt.txt && \\
python audio_effects.py \\
    --input temp.wav \\
    --reverb 0.3 \\
    --output final.wav

# Profile performance
python main.py \\
    --image test.jpg \\
    --profile \\
    --output profile_test.wav 2> timing.log"""
        render_code_with_copy(advanced_code, "bash", "advanced_workflow")

def render_api_section():
    """Render Web API documentation and testing interface"""
    st.markdown("## 🌐 Web API")
    st.markdown("Mozart's Touch includes a FastAPI-based web interface for remote access.")
    
    st.markdown("### 🚀 Starting the Server")
    
    server_code = """# Start the API server
python api_server.py --host 0.0.0.0 --port 8000

# With auto-reload for development
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000

# With custom configuration
python api_server.py \\
    --config production_config.yaml \\
    --workers 4 \\
    --ssl-keyfile key.pem \\
    --ssl-certfile cert.pem"""
    render_code_with_copy(server_code, "bash", "api_server_start")
    
    st.markdown("---")
    st.markdown("### 📚 API Endpoints")
    
    endpoints = [
        {
            "method": "POST",
            "path": "/generate/image",
            "description": "Generate music from an uploaded image",
            "request": """{
  "file": "<image_file>",
  "duration": 15,
  "model": "medium",
  "guidance_scale": 3.5,
  "format": "wav"
}""",
            "response": """{
  "success": true,
  "audio_url": "/download/abc123.wav",
  "caption": "A beautiful sunset over the ocean...",
  "prompt": "Calm, atmospheric music with...",
  "duration": 15.0,
  "processing_time": 12.34
}"""
        },
        {
            "method": "POST",
            "path": "/generate/video",
            "description": "Generate music from an uploaded video",
            "request": """{
  "file": "<video_file>",
  "sync_length": true,
  "fps_sample": 1.0,
  "model": "large"
}""",
            "response": """{
  "success": true,
  "audio_url": "/download/xyz789.wav",
  "frames_analyzed": 24,
  "video_duration": 30.0,
  "audio_duration": 30.0
}"""
        },
        {
            "method": "POST",
            "path": "/generate/prompt",
            "description": "Generate music from a text prompt directly",
            "request": """{
  "prompt": "Upbeat electronic music with synth leads",
  "duration": 20,
  "guidance_scale": 4.0
}""",
            "response": """{
  "success": true,
  "audio_url": "/download/prompt123.wav",
  "duration": 20.0
}"""
        },
        {
            "method": "GET",
            "path": "/status",
            "description": "Get server status and model information",
            "request": "N/A",
            "response": """{
  "status": "healthy",
  "models_loaded": ["musicgen-medium", "blip2"],
  "gpu_available": true,
  "gpu_memory_used": "4.2 GB",
  "queue_length": 0
}"""
        }
    ]
    
    for endpoint in endpoints:
        with st.expander(f"**`{endpoint['method']}`** `{endpoint['path']}`"):
            st.markdown(f"_{endpoint['description']}_")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Request:**")
                st.code(endpoint["request"], language="json")
            
            with col2:
                st.markdown("**Response:**")
                st.code(endpoint["response"], language="json")
    
    st.markdown("---")
    st.markdown("### 🧪 API Testing Interface")
    
    test_tabs = st.tabs(["Image Generation", "Text Prompt", "Status Check"])
    
    with test_tabs[0]:
        st.markdown("#### Test Image-to-Music Generation")
        
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Select an image to generate music from"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            test_duration = st.slider("Duration (seconds)", 5, 30, 10, key="test_duration")
            test_model = st.selectbox("Model", ["small", "medium", "large"], key="test_model")
        
        with col2:
            test_guidance = st.slider("Guidance Scale", 1.0, 10.0, 3.0, key="test_guidance")
            test_format = st.selectbox("Format", ["wav", "mp3", "flac"], key="test_format")
        
        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", width=300)
        
        if st.button("🎵 Generate Music", key="gen_image"):
            if uploaded_file:
                with st.spinner("Generating music... (Demo Mode)"):
                    time.sleep(2)
                    st.success("Music generated successfully!")
                    st.info("In production, this would return the generated audio file.")
                    
                    st.markdown("**Simulated Response:**")
                    st.json({
                        "success": True,
                        "caption": "A vibrant landscape with rolling hills...",
                        "prompt": "Peaceful, uplifting orchestral music...",
                        "duration": test_duration,
                        "model": test_model
                    })
            else:
                st.warning("Please upload an image first.")
    
    with test_tabs[1]:
        st.markdown("#### Test Text-to-Music Generation")
        
        prompt_input = st.text_area(
            "Enter your music prompt",
            value="Calm ambient music with soft piano and gentle strings, suitable for meditation",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            prompt_duration = st.slider("Duration (seconds)", 5, 60, 15, key="prompt_duration")
        
        with col2:
            prompt_guidance = st.slider("Guidance Scale", 1.0, 10.0, 3.5, key="prompt_guidance")
        
        if st.button("🎵 Generate from Prompt", key="gen_prompt"):
            with st.spinner("Generating music... (Demo Mode)"):
                time.sleep(2)
                st.success("Music generated successfully!")
                
                st.markdown("**cURL equivalent:**")
                curl_code = f"""curl -X POST "http://localhost:8000/generate/prompt" \\
    -H "Content-Type: application/json" \\
    -d '{{"prompt": "{prompt_input[:50]}...", "duration": {prompt_duration}, "guidance_scale": {prompt_guidance}}}'"""
                render_code_with_copy(curl_code, "bash", "curl_prompt")
    
    with test_tabs[2]:
        st.markdown("#### Check Server Status")
        
        if st.button("🔍 Check Status", key="check_status"):
            st.json({
                "status": "healthy",
                "version": "1.0.0",
                "models_loaded": ["facebook/musicgen-medium", "Salesforce/blip2-opt-2.7b"],
                "gpu_available": True,
                "gpu_name": "NVIDIA RTX 4090",
                "gpu_memory_total": "24 GB",
                "gpu_memory_used": "6.2 GB",
                "queue_length": 0,
                "uptime": "2h 34m 12s"
            })

def render_examples():
    """Render example use cases"""
    st.markdown("## 🎯 Example Use Cases")
    
    examples = [
        {
            "title": "Nature Photography to Ambient Music",
            "description": "Transform landscape photos into relaxing ambient soundscapes",
            "input_desc": "Sunrise over mountains with mist",
            "output_desc": "Ethereal ambient music with soft pads and nature-inspired textures",
            "config": {
                "model": "musicgen-medium",
                "duration": 30,
                "guidance_scale": 3.5,
                "temperature": 0.9
            },
            "icon": "🏔️"
        },
        {
            "title": "Urban Street Photography to Lo-Fi",
            "description": "Convert city scenes into chill lo-fi beats",
            "input_desc": "Rainy city street at night with neon lights",
            "output_desc": "Lo-fi hip hop with vinyl crackle, mellow keys, and subtle rain sounds",
            "config": {
                "model": "musicgen-large",
                "duration": 45,
                "guidance_scale": 4.0,
                "temperature": 1.1
            },
            "icon": "🌃"
        },
        {
            "title": "Action Sports Video Soundtrack",
            "description": "Generate high-energy music for extreme sports footage",
            "input_desc": "Mountain biking downhill video",
            "output_desc": "Intense electronic rock with driving drums and energetic synths",
            "config": {
                "model": "musicgen-large",
                "sync_length": True,
                "guidance_scale": 5.0,
                "temperature": 0.8
            },
            "icon": "🚴"
        },
        {
            "title": "Product Photography for Ads",
            "description": "Create background music for product showcase videos",
            "input_desc": "Luxury watch on marble surface",
            "output_desc": "Sophisticated, minimal electronic music with elegant piano accents",
            "config": {
                "model": "musicgen-medium",
                "duration": 20,
                "guidance_scale": 3.0,
                "temperature": 0.7
            },
            "icon": "⌚"
        }
    ]
    
    for example in examples:
        with st.expander(f"{example['icon']} {example['title']}", expanded=False):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Input Description:**")
                st.info(example["input_desc"])
                
                st.markdown("**Expected Output:**")
                st.success(example["output_desc"])
            
            with col2:
                st.markdown("**Recommended Configuration:**")
                st.code(json.dumps(example["config"], indent=2), language="json")
            
            st.markdown("**Command:**")
            cmd_code = f"""python main.py \\
    --image example_{example['icon']}.jpg \\
    --output {example['title'].lower().replace(' ', '_')}.wav \\
    --model {example['config']['model']} \\
    --duration {example['config'].get('duration', 30)} \\
    --guidance {example['config']['guidance_scale']}"""
            render_code_with_copy(cmd_code, "bash", f"example_{example['title'].replace(' ', '_')}")
    
    st.markdown("---")
    st.markdown("### 🎨 Sample Prompts Gallery")
    
    prompt_categories = {
        "Nature & Landscapes": [
            "Peaceful forest ambience with birdsong and gentle breeze",
            "Majestic ocean waves crashing on rocky cliffs at sunset",
            "Serene mountain lake reflecting autumn colors"
        ],
        "Urban & City": [
            "Busy downtown street with jazz club atmosphere",
            "Rainy afternoon in a cozy coffee shop",
            "Neon-lit cyberpunk cityscape at midnight"
        ],
        "Abstract & Artistic": [
            "Flowing watercolors merging in slow motion",
            "Geometric patterns pulsing with electronic rhythm",
            "Dreamlike surrealist landscape with melting clocks"
        ],
        "Emotional & Mood": [
            "Nostalgic memories of childhood summers",
            "Triumphant victory after long struggle",
            "Quiet contemplation during starlit night"
        ]
    }
    
    cols = st.columns(2)
    
    for idx, (category, prompts) in enumerate(prompt_categories.items()):
        with cols[idx % 2]:
            st.markdown(f"**{category}**")
            for prompt in prompts:
                st.markdown(f"""
                <div style="padding: 0.5rem; background: rgba(45, 45, 63, 0.5); border-radius: 8px; margin: 0.25rem 0; font-size: 0.875rem; color: #94A3B8;">
                    {prompt}
                </div>
                """, unsafe_allow_html=True)

def render_troubleshooting():
    """Render troubleshooting section"""
    st.markdown("## ❓ Troubleshooting")
    
    issues = [
        {
            "title": "CUDA Out of Memory Error",
            "symptoms": ["RuntimeError: CUDA out of memory", "GPU memory allocation failed"],
            "solutions": [
                "Use a smaller model (e.g., musicgen-small instead of large)",
                "Reduce batch size or duration",
                "Enable gradient checkpointing",
                "Use CPU inference as fallback"
            ],
            "code": """# Use smaller model
python main.py --image input.jpg --model small

# Force CPU inference
python main.py --image input.jpg --device cpu

# Clear GPU cache before running
python -c "import torch; torch.cuda.empty_cache()"
python main.py --image input.jpg"""
        },
        {
            "title": "Model Download Fails",
            "symptoms": ["Connection timeout", "HTTP 403 Forbidden", "Repository not found"],
            "solutions": [
                "Check your Hugging Face token is valid",
                "Ensure you have accepted model licenses on HF Hub",
                "Try using a VPN if in restricted region",
                "Download models manually"
            ],
            "code": """# Set HuggingFace token
export HF_TOKEN="your-token-here"

# Login to HuggingFace CLI
huggingface-cli login

# Manual download
git lfs install
git clone https://huggingface.co/facebook/musicgen-small ./models/musicgen-small"""
        },
        {
            "title": "Audio Output Issues",
            "symptoms": ["Silent output", "Corrupted audio file", "Wrong duration"],
            "solutions": [
                "Verify soundfile/scipy installation",
                "Check output directory permissions",
                "Try different audio format",
                "Inspect intermediate files if saved"
            ],
            "code": """# Test audio writing
python -c "
import numpy as np
import soundfile as sf
audio = np.random.randn(32000).astype(np.float32)
sf.write('test.wav', audio, 32000)
print('Audio write test passed!')
"

# Use different format
python main.py --image input.jpg --format flac"""
        },
        {
            "title": "OpenAI API Errors",
            "symptoms": ["API key invalid", "Rate limit exceeded", "Connection refused"],
            "solutions": [
                "Verify OPENAI_API_KEY environment variable",
                "Check API quota and billing status",
                "Implement retry logic for rate limits",
                "Use local LLM as alternative"
            ],
            "code": """# Verify API key
echo $OPENAI_API_KEY

# Test API connection
python -c "
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello'}]
)
print('API connection successful!')
"

# Use template mode instead (no LLM required)
python main.py --image input.jpg --converter-type template"""
        },
        {
            "title": "Video Processing Errors",
            "symptoms": ["Cannot open video file", "Frame extraction failed", "Codec not supported"],
            "solutions": [
                "Install ffmpeg on your system",
                "Update opencv-python package",
                "Convert video to common format (mp4/h264)",
                "Reduce video resolution"
            ],
            "code": """# Install ffmpeg
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS

# Convert video format
ffmpeg -i input.avi -c:v libx264 -crf 23 output.mp4

# Test video reading
python -c "
import cv2
cap = cv2.VideoCapture('video.mp4')
ret, frame = cap.read()
print(f'Video opened: {ret}, Frame shape: {frame.shape if ret else None}')
cap.release()
"
"""
        }
    ]
    
    for issue in issues:
        with st.expander(f"⚠️ {issue['title']}", expanded=False):
            st.markdown("**Common Symptoms:**")
            for symptom in issue["symptoms"]:
                st.markdown(f"- `{symptom}`")
            
            st.markdown("**Solutions:**")
            for i, solution in enumerate(issue["solutions"], 1):
                st.markdown(f"{i}. {solution}")
            
            st.markdown("**Code Fix:**")
            render_code_with_copy(issue["code"], "bash", f"fix_{issue['title'].replace(' ', '_')}")
    
    st.markdown("---")
    st.markdown("### 📞 Getting Help")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(45, 45, 63, 0.5); border-radius: 12px; text-align: center;">
            <span style="font-size: 2rem;">📖</span>
            <h4 style="color: #E2E8F0; margin: 0.5rem 0;">Documentation</h4>
            <p style="color: #94A3B8; font-size: 0.875rem;">Check the full docs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(45, 45, 63, 0.5); border-radius: 12px; text-align: center;">
            <span style="font-size: 2rem;">💬</span>
            <h4 style="color: #E2E8F0; margin: 0.5rem 0;">GitHub Issues</h4>
            <p style="color: #94A3B8; font-size: 0.875rem;">Report bugs & requests</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(45, 45, 63, 0.5); border-radius: 12px; text-align: center;">
            <span style="font-size: 2rem;">💡</span>
            <h4 style="color: #E2E8F0; margin: 0.5rem 0;">Discord Community</h4>
            <p style="color: #94A3B8; font-size: 0.875rem;">Join the discussion</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    sidebar_navigation()
    
    section = st.session_state.get("current_section", "overview")
    
    if section == "overview":
        render_overview()
    elif section == "prerequisites":
        render_prerequisites()
    elif section == "config":
        render_config_wizard()
    elif section == "dependencies":
        render_dependencies()
    elif section == "installation":
        render_installation()
    elif section == "cli":
        render_cli_usage()
    elif section == "api":
        render_api_section()
    elif section == "examples":
        render_examples()
    elif section == "troubleshooting":
        render_troubleshooting()
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #64748B;">
        <p>Mozart's Touch Interactive Guide | Built with Streamlit</p>
        <p style="font-size: 0.75rem;">© 2025 Mozart's Touch Project | MIT License</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
