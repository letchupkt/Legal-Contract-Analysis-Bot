

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from werkzeug.utils import secure_filename
import os
import tempfile
import json
import base64
from io import BytesIO
import uuid
from dotenv import load_dotenv


from nlp import extract_text_from_pdf, extract_text_from_docx, clean_text, split_into_clauses
from llm import call_gpt4_for_clause, call_gpt4_summary, ask_question_about_contract
from scoring import overall_risk_score
from utils import create_pdf_report, highlight_text_html


load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.getenv('SECRET_KEY', 'legal-risk-bot-secret-key-2024')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024     # 16 MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Use PDF, DOCX, or TXT files.'}), 400
        
       
        filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
        file.save(file_path)
        
     
        try:
            if filename.lower().endswith('.pdf'):
                raw_text = extract_text_from_pdf(file_path)
            elif filename.lower().endswith('.docx'):
                raw_text = extract_text_from_docx(file_path)
            else:  # txt file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    raw_text = f.read()
            
           
            raw_text = clean_text(raw_text)
            
         
            session['contract_text'] = raw_text
            session['filename'] = filename
            session['file_id'] = file_id
            
    
            os.remove(file_path)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'text_preview': raw_text[:2000] + ("..." if len(raw_text) > 2000 else ""),
                'text_length': len(raw_text)
            })
            
        except Exception as e:
          
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_contract():

    try:
        if 'contract_text' not in session:
            return jsonify({'error': 'No contract uploaded'}), 400
        
        data = request.get_json()
        max_clauses = data.get('max_clauses', 6)
        model = data.get('model', 'gpt-4')
        language = data.get('language', 'English')
        
       
        supported_models = [
            'gpt-4', 'gpt-3.5-turbo', 
            'claude-3-sonnet', 'claude-3-haiku', 
            'gemini-2.0-flash', 'gemini-pro', 
            'ollama-gemma2:27b', 'ollama-gemma-2b-lawer:latest', 
            'ollama-Gemma-2-2B-Indian-Law-Q8:latest', 'ollama-gemma:2b'
        ]
        if model not in supported_models:
            return jsonify({'error': f'Unsupported model: {model}. Supported models: {supported_models}'}), 400
        
        contract_text = session['contract_text']
        
      
        clauses = split_into_clauses(contract_text, max_clause_len=900)
        clauses_to_analyze = clauses[:max_clauses]
        
   
        results = []
        for idx, clause in enumerate(clauses_to_analyze):
            try:
                
                parsed = call_gpt4_for_clause(clause, model=model, language=language)
                result = {
                    "clause": clause,
                    "explanation": parsed.get("explanation", ""),
                    "risk": parsed.get("risk", "Medium"),
                    "suggestion": parsed.get("suggestion", "")
                }
                
                results.append(result)
                
            except Exception as e:
            
                error_msg = f"Error analyzing clause: {str(e)}"
                if language == "Hindi":
                    error_msg = f"खंड विश्लेषण में त्रुटि: {str(e)}"
                elif language == "Tamil":
                    error_msg = f"பிரிவு பகுப்பாய்வில் பிழை: {str(e)}"
                
                results.append({
                    "clause": clause,
                    "explanation": error_msg,
                    "risk": "Medium",
                    "suggestion": "Please review manually" if language == "English" else 
                                 "कृपया मैन्युअल रूप से समीक्षा करें" if language == "Hindi" else
                                 "தயவுசெய்து கைமுறையாக மதிப்பாய்வு செய்யுங்கள்"
                })
        
   
        overall_score = overall_risk_score(results)
        
        
        session['analysis_results'] = results
        session['overall_score'] = overall_score
        session['language'] = language
        
        return jsonify({
            'success': True,
            'results': results,
            'overall_score': overall_score,
            'total_clauses': len(clauses),
            'analyzed_clauses': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/summary', methods=['POST'])
def generate_summary():
    
    try:
        if 'contract_text' not in session:
            return jsonify({'error': 'No contract uploaded'}), 400
        
        data = request.get_json()
        language = data.get('language', session.get('language', 'English'))
        model = data.get('model', 'gpt-4')
        
        contract_text = session['contract_text']
        
        
        summary = call_gpt4_summary(contract_text[:4000], model=model, language=language)
        
        session['summary'] = summary
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': f'Summary generation failed: {str(e)}'}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    
    try:
        if 'analysis_results' not in session:
            return jsonify({'error': 'No analysis available. Please analyze the contract first.'}), 400
        
        data = request.get_json()
        question = data.get('question', '').strip()
        language = data.get('language', session.get('language', 'English'))
        
        if not question:
            return jsonify({'error': 'Please provide a question'}), 400
        
        results = session['analysis_results']
        model = data.get('model', 'gpt-4')
        
    
        answer_text = ask_question_about_contract(question, results, model=model, language=language)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer_text
        })
        
    except Exception as e:
        return jsonify({'error': f'Q&A failed: {str(e)}'}), 500

@app.route('/export-pdf')
def export_pdf():
    
    try:
        if 'analysis_results' not in session:
            return jsonify({'error': 'No analysis available'}), 400
        
        results = session['analysis_results']
        overall_score = session.get('overall_score', 0)
        summary = session.get('summary', 'No summary generated')
        filename = session.get('filename', 'contract')
        
        # Generate PDF 
        pdf_bytes = create_pdf_report(summary, overall_score, results)
        
        # Create a BytesIO object
        pdf_buffer = BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        # Generate filename
        safe_filename = secure_filename(filename.rsplit('.', 1)[0] if '.' in filename else filename)
        pdf_filename = f"{safe_filename}_risk_analysis.pdf"
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=pdf_filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'PDF export failed: {str(e)}'}), 500

@app.route('/highlight')
def get_highlighted_contract():
  
    try:
        if 'contract_text' not in session or 'analysis_results' not in session:
            return jsonify({'error': 'No contract or analysis available'}), 400
        
        contract_text = session['contract_text']
        results = session['analysis_results']
        
        # Generate highlighted HTML 
        highlighted_html = highlight_text_html(contract_text[:8000], results)
        
        return jsonify({
            'success': True,
            'highlighted_html': highlighted_html
        })
        
    except Exception as e:
        return jsonify({'error': f'Highlighting failed: {str(e)}'}), 500

@app.route('/reset')
def reset_session():
    """Reset the session"""
    session.clear()
    return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    

    app.run(debug=True, host='0.0.0.0', port=5000)