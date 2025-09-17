

import os
import subprocess
import sys

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ollama_models():
    """Install required Ollama models"""
    models = ['gemma2:2b']
    local_models = ['Gemma-2-2B-Indian-Law-Q8:latest']  # Models already available locally
    
    if not check_ollama_installed():
        print("❌ Ollama is not installed!")
        print("📥 Please install Ollama from: https://ollama.ai/")
        print("💡 After installation, run this script again to download models")
        return False
    
    print("✅ Ollama is installed!")
    print("📥 Installing required models...")
    print("⚠️  Note: Large models like Gemma2 27B may take time to download")
    
    # Install downloadable models
    for model in models:
        print(f"🔄 Downloading {model}...")
        try:
            result = subprocess.run(['ollama', 'pull', model], check=True)
            print(f"✅ {model} installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {model}: {e}")
            print(f"💡 You can manually install it later with: ollama pull {model}")
            continue
    
    # Check local models
    print("\n📋 Checking local models...")
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
        available_models = result.stdout
        
        for model in local_models:
            if model in available_models:
                print(f"✅ {model} is available locally!")
            else:
                print(f"⚠️  {model} not found locally. Please ensure it's properly installed.")
    except subprocess.CalledProcessError:
        print("❌ Could not check local models")
    
    return True

def check_api_keys():
    """Check if API keys are configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    print("\n🔑 API Key Status:")
    print(f"OpenAI: {'✅ Configured' if openai_key and openai_key != 'your_openai_api_key_here' else '❌ Not configured'}")
    print(f"Anthropic (Claude): {'✅ Configured' if anthropic_key and anthropic_key != 'your_anthropic_api_key_here' else '❌ Not configured'}")
    print(f"Gemini (2.0 Flash/Pro): {'✅ Configured' if gemini_key and gemini_key != 'your_gemini_api_key_here' else '❌ Not configured'}")
    print(f"Ollama: {'✅ Local models (no API key needed)' if check_ollama_installed() else '❌ Not installed'}")
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("\n💡 To use OpenAI models (GPT-4, GPT-3.5):")
        print("   1. Get API key from: https://platform.openai.com/api-keys")
        print("   2. Update OPENAI_API_KEY in .env file")
    
    if not anthropic_key or anthropic_key == 'your_anthropic_api_key_here':
        print("\n💡 To use Claude 3 models:")
        print("   1. Get API key from: https://console.anthropic.com/")
        print("   2. Update ANTHROPIC_API_KEY in .env file")
    
    if not gemini_key or gemini_key == 'your_gemini_api_key_here':
        print("\n💡 To use Gemini models (2.0 Flash, Pro):")
        print("   1. Get API key from: https://makersuite.google.com/app/apikey")
        print("   2. Update GEMINI_API_KEY in .env file")

def main():
    print("🏛️ Legal Contract Bot - Model Setup")
    print("=" * 50)
    
    # Check and install Ollama models
    print("\n📦 Setting up Ollama models...")
    install_ollama_models()
    
    # Check API keys
    check_api_keys()
    
    print("\n🎉 Setup complete!")
    print("🚀 You can now run the application with: python app.py")

if __name__ == "__main__":
    main()