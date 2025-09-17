

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def download_spacy_model():
    """Download spaCy English model"""
    return run_command("python -m spacy download en_core_web_sm", "Downloading spaCy model")

def setup_environment():
    """Setup environment file"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("🔧 Setting up environment...")
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key or not api_key.startswith("sk-"):
        print("❌ Invalid API key format")
        return False
    
    try:
        with open(".env", "w") as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
            f.write("SECRET_KEY=legal-contract-bot-2024\n")
        print("✅ Environment configured")
        return True
    except Exception as e:
        print(f"❌ Environment setup failed: {e}")
        return False

def verify_installation():
    """Verify the installation"""
    print("🧪 Verifying installation...")
    try:
        from flask_app import app
        from nlp import split_into_clauses
        from llm import call_gpt4_for_clause
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import verification failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🏛️ Legal Contract Analysis Bot - Setup")
    print("=" * 50)
    
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    if not download_spacy_model():
        print("❌ spaCy model download failed")
        sys.exit(1)
    
    if not setup_environment():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    if not verify_installation():
        print("❌ Installation verification failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n🚀 To run the application:")
    print("   python app.py")
    print("\n🌐 Then open: http://localhost:5000")

if __name__ == "__main__":
    main()