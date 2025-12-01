
#!/bin/bash

echo "🎵 Setting up Phin Isan AI..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo "❌ Python 3.8+ is required. You have Python $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Install dependencies
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys"
fi

# Create output directories
echo "📁 Creating output directories..."
mkdir -p outputs/audio
mkdir -p outputs/midi
mkdir -p outputs/logs

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OPENAI_API_KEY"
echo "2. Run: python main.py --help"
echo "3. Or start the web UI: streamlit run app.py --server.port 5000"
