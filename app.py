

from flask_app import app
import os

if __name__ == '__main__':
    print("🏛️ Legal Contract Analysis Bot")
    print("=" * 40)
    print("🚀 Starting Flask server...")
    print("🌐 Access: http://localhost:5000")
    print("📱 Features: Comprehensive AI Analysis, Professional PDF Reports, Enhanced Highlighting, TTS Support")
    print("⌨️  Press Ctrl+C to stop")
    print("=" * 40)
    
    # Ensure upload directory exists
    os.makedirs(app.config.get('UPLOAD_FOLDER', '/tmp'), exist_ok=True)
    

    app.run(debug=True, host='0.0.0.0', port=5000)