# Legal Contract Analysis Bot ⚖️

A complete AI-powered web application prototype that helps small business owners in India understand complex legal contracts through automated analysis, risk assessment, and plain-language explanations.

## 🎯 Project Overview

This is a **complete working prototype** built for hackathons and demonstrations. It features a professional Flask web application with AI-powered contract analysis, risk assessment, and multilingual support.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
python setup.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env

# Test installation
python test.py

# Run application
python app.py
```

### Setup AI Models
```bash
# Setup all AI models (optional)
python setup_models.py
```

### Access the Application
Open your browser to: **http://localhost:5000**

## ✨ Complete Feature Set

### 🎨 Professional Web Interface
- **Dark Theme**: Modern glass-morphism design
- **Responsive Layout**: Works on desktop, tablet, mobile
- **Real-time Updates**: Live progress indicators
- **Interactive Elements**: Smooth animations and transitions

### 📄 Document Processing
- **Multi-format Support**: PDF, DOCX, TXT files
- **Drag & Drop Upload**: Intuitive file interface
- **Text Extraction**: Advanced document parsing
- **File Validation**: Secure file handling

### 🤖 Multi-Model AI Analysis
- **OpenAI Models**: GPT-4, GPT-3.5 Turbo support
- **Anthropic Claude 3**: Sonnet & Haiku models
- **Google Gemini**: Gemini 2.0 Flash & Pro integration
- **Ollama Support**: Local models (Gemma2 27B, Llama3.1 8B, Mistral)
- **Model Selection**: Choose the best AI for your needs
- **Clause Detection**: Intelligent contract segmentation
- **Risk Assessment**: Three-tier classification (Low/Medium/High)
- **Plain Language**: Complex legal terms simplified

### 🌐 Multilingual Support
- **English**: Full analysis in English
- **Hindi Translation**: AI-powered Hindi translation
- **Tamil Translation**: AI-powered Tamil translation
- **Cultural Context**: India-specific legal considerations
- **Language Toggle**: Easy switching between languages

### 📊 Visual Analytics
- **Risk Dashboard**: Color-coded risk indicators
- **Overall Score**: Percentage-based risk assessment
- **Interactive Cards**: Animated analysis results
- **Progress Tracking**: Real-time analysis feedback

### 💬 Interactive Q&A
- **AI Assistant**: Ask questions about contract clauses
- **Context-Aware**: Responses based on analyzed content
- **Business-Focused**: Tailored for SME concerns
- **Multilingual**: Questions and answers in both languages

### 📋 Export & Reporting
- **PDF Reports**: Professional analysis reports
- **Contract Highlighting**: Visual markup of risky clauses
- **Summary Generation**: AI-powered contract summaries
- **Download Options**: Multiple export formats

## 🏗️ Clean Project Structure

```
legal-contract-analysis-bot/
├── 📱 Core Application
│   ├── app.py                 # Main application entry point
│   ├── flask_app.py          # Flask web server
│   ├── setup.py              # Automated setup script
│   └── test.py               # Comprehensive test suite
│
├── 🧠 AI & Processing
│   ├── llm.py                # OpenAI GPT-4 integration
│   ├── nlp.py                # Text processing & NLP
│   ├── scoring.py            # Risk assessment logic
│   └── utils.py              # Utility functions
│
├── 🎨 Frontend
│   ├── templates/
│   │   └── index.html        # Main UI template (with embedded CSS)
│   └── static/
│       └── style.css         # Additional CSS (optional)
│
├── 📄 Sample Data
│   └── sample_contracts/
│       ├── employment_sample.txt
│       ├── service_sample.txt
│       └── vendor_sample.txt
│
├── ⚙️ Configuration
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables
│   └── README.md            # This file
│
└── 📚 Documentation
    └── DOCUMENTATION.md      # Complete technical docs
```

## 🔧 Technology Stack

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **AI/ML**: Multi-model support
  - OpenAI GPT-4 & GPT-3.5 Turbo
  - Anthropic Claude 3 (Sonnet & Haiku)
  - Google Gemini 2.0 Flash & Pro
  - Ollama (Local models: Gemma2 27B, Llama3.1 8B, Mistral)
- **NLP**: spaCy for text processing
- **Document Processing**: PyMuPDF, python-docx
- **Report Generation**: ReportLab
- **Styling**: Custom CSS with dark theme

## 🎯 Demo Features

Perfect for hackathon demonstrations:

1. **Live File Upload**: Drag and drop contracts
2. **Real-time Analysis**: Watch AI analyze clauses
3. **Visual Results**: Color-coded risk assessment
4. **Interactive Q&A**: Ask questions about contracts
5. **Multilingual Demo**: Switch between English and Hindi
6. **Export Functionality**: Generate PDF reports
7. **Professional UI**: Modern, responsive design

## 📊 Performance

- **Analysis Speed**: 30-180 seconds (depending on contract size)
- **File Support**: Up to 16MB files
- **Concurrent Users**: Supports multiple users
- **Response Time**: < 2 seconds for most operations
- **Mobile Ready**: Responsive design for all devices

## 🧪 Testing

```bash
# Run comprehensive tests
python test.py

# Test specific components
python -c "from nlp import split_into_clauses; print('NLP working')"
python -c "from flask_app import app; print('Flask working')"
```

## 🚀 Deployment Ready

### Local Development
```bash
python app.py  # Runs on http://localhost:5000
```

### Production Deployment
- **Docker**: Container-ready
- **Cloud**: AWS, GCP, Azure compatible
- **Heroku**: Direct deployment support
- **VPS**: Standard Flask deployment

## 🔒 Security Features

- **File Validation**: Strict file type checking
- **Size Limits**: Prevents large file attacks
- **Session Management**: Secure user sessions
- **API Key Protection**: Environment-based configuration
- **Error Handling**: Comprehensive error management

## 🎨 UI/UX Highlights

- **Dark Theme**: Professional appearance
- **Glass Morphism**: Modern translucent effects
- **Gradient Elements**: Eye-catching buttons and text
- **Color Coding**: Intuitive risk visualization
- **Smooth Animations**: Professional transitions
- **Mobile First**: Responsive design approach

## 📋 Sample Contracts Included

- **Employment Agreement**: Standard employment contract
- **Service Contract**: Service provider agreement
- **Vendor Agreement**: Supplier/vendor contract

## 🛡️ Legal Disclaimer

This application provides informational analysis only and does not constitute legal advice. Users should consult qualified legal professionals for specific legal matters.

## 🆘 Troubleshooting

### Common Issues
- **API Key**: Ensure valid OpenAI API key in .env
- **Dependencies**: Run `python setup.py` to install all requirements
- **spaCy Model**: Download with `python -m spacy download en_core_web_sm`
- **Port Conflict**: Change port in app.py if 5000 is in use

### AI Model Configuration

#### OpenAI Models (GPT-4, GPT-3.5)
1. Get API key from: https://platform.openai.com/api-keys
2. Add to .env: `OPENAI_API_KEY=your_key_here`

#### Anthropic Claude 3 (Sonnet, Haiku)
1. Get API key from: https://console.anthropic.com/
2. Add to .env: `ANTHROPIC_API_KEY=your_key_here`

#### Google Gemini (2.0 Flash, Pro)
1. Get API key from: https://makersuite.google.com/app/apikey
2. Add to .env: `GEMINI_API_KEY=your_key_here`

#### Ollama (Local Models)
1. Install Ollama: https://ollama.ai/
2. Run: `python setup_models.py` to download models
3. No API key needed (runs locally)
4. Models: Gemma2 27B, Llama3.1 8B, Mistral

## 🔧 Model Selection Guide:

### Cloud Models (API Required)
- **GPT-4**: Highest quality, most expensive, excellent reasoning
- **GPT-3.5 Turbo**: Good quality, faster, cost-effective
- **Claude 3 Sonnet**: Excellent reasoning, balanced performance
- **Claude 3 Haiku**: Fast, efficient, good for simple analysis
- **Gemini 2.0 Flash**: Google's latest, fastest model with multimodal capabilities
- **Gemini Pro**: Google's established competitive alternative

### Local Models (Free, Private)
- **Ollama Gemma2 27B**: Google's powerful local model, excellent quality
- **Ollama Llama3.1 8B**: Meta's latest, good balance of speed/quality
- **Ollama Mistral**: Fast, efficient, good reasoning capabilities

### Getting Help
1. Run `python test.py` for diagnostics
2. Run `python setup_models.py` for model setup
3. Check browser console for JavaScript errors
4. Review Flask logs for server issues
5. Test with sample contracts first

---

**Built with ❤️ by CodeSentinels | Empowering Indian SMEs with AI-powered legal technology**
