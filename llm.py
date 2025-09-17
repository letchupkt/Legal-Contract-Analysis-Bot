
import os
import time
from openai import OpenAI
import google.generativeai as genai
import anthropic
import ollama
from typing import Dict, Tuple, List
import json
from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
if ANTHROPIC_API_KEY:
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


CLAUSE_ANALYSIS_PROMPT_ENGLISH = """
You are a legal assistant for small and medium business owners in India.
Analyze the following contract clause thoroughly and provide comprehensive analysis.

Clause:
\"\"\"{clause}\"\"\"

Provide detailed analysis in JSON format with keys:
- explanation: Comprehensive plain-English explanation covering all legal implications, potential issues, and business impact. Be thorough and detailed.
- risk: one of ["Low","Medium","High"] based on potential business impact.
- suggestion: Detailed safer alternative clause or specific mitigation strategies .

Be comprehensive and detailed in your analysis. Respond ONLY with valid JSON.
"""

CLAUSE_ANALYSIS_PROMPT_HINDI = """
आप भारत के छोटे और मध्यम व्यापारियों के लिए एक कानूनी सहायक हैं।
निम्नलिखित अनुबंध खंड का विस्तृत विश्लेषण करें।

खंड:
\"\"\"{clause}\"\"\"

JSON प्रारूप में विस्तृत विश्लेषण प्रदान करें:
- explanation: व्यापक हिंदी में स्पष्टीकरण जिसमें सभी कानूनी निहितार्थ, संभावित समस्याएं और व्यापारिक प्रभाव शामिल हों। विस्तृत और संपूर्ण रहें।
- risk: व्यापारिक प्रभाव के आधार पर ["Low","Medium","High"] में से एक।
- suggestion: विस्तृत सुरक्षित वैकल्पिक खंड या विशिष्ट जोखिम कम करने की रणनीतियां.

अपने विश्लेषण में व्यापक और विस्तृत रहें। केवल वैध JSON के साथ उत्तर दें।
"""

CLAUSE_ANALYSIS_PROMPT_TAMIL = """
நீங்கள் இந்தியாவின் சிறு மற்றும் நடுத்தர வணிகர்களுக்கான சட்ட உதவியாளர்.
பின்வரும் ஒப்பந்த பிரிவின் விரிவான பகுப்பாய்வு செய்யுங்கள்.

பிரிவு:
\"\"\"{clause}\"\"\"

JSON வடிவத்தில் விரிவான பகுப்பாய்வு வழங்கவும்:
- explanation: விரிவான தமிழ் விளக்கம் அனைத்து சட்ட தாக்கங்கள், சாத்தியமான பிரச்சினைகள் மற்றும் வணிக தாக்கத்தை உள்ளடக்கியது. முழுமையாகவும் விரிவாகவும் இருங்கள்.
- risk: வணிக தாக்கத்தின் அடிப்படையில் ["Low","Medium","High"] இல் ஒன்று.
- suggestion: விரிவான பாதுகாப்பான மாற்று பிரிவு அல்லது குறிப்பிட்ட ஆபத்து குறைப்பு உத்திகள்.

உங்கள் பகுப்பாய்வில் விரிவாகவும் முழுமையாகவும் இருங்கள். செல்லுபடியாகும் JSON மட்டுமே பதிலளிக்கவும்.
"""

SUMMARY_PROMPT_ENGLISH = """
You are a legal assistant for Indian SMEs. Provide a comprehensive contract summary.

Contract text:
\"\"\"{contract}\"\"\"

Provide a detailed summary covering:
1. Main parties and their obligations
2. Key terms and conditions
3. Payment and delivery terms
4. Risk factors and potential issues
5. Termination clauses
6. Specific recommendations for the business owner

Write in clear, business-friendly English.
"""

SUMMARY_PROMPT_HINDI = """
आप भारतीय छोटे और मध्यम उद्यमों के लिए एक कानूनी सहायक हैं। व्यापक अनुबंध सारांश प्रदान करें।

अनुबंध पाठ:
\"\"\"{contract}\"\"\"

विस्तृत सारांश प्रदान करें जिसमें शामिल हो:
1. मुख्य पक्ष और उनके दायित्व
2. मुख्य नियम और शर्तें
3. भुगतान और डिलीवरी की शर्तें
4. जोखिम कारक और संभावित समस्याएं
5. समाप्ति खंड
6. व्यापारी के लिए विशिष्ट सिफारिशें

स्पष्ट, व्यापार-अनुकूल हिंदी में लिखें।
"""

SUMMARY_PROMPT_TAMIL = """
நீங்கள் இந்திய சிறு மற்றும் நடுத்தர நிறுவனங்களுக்கான சட்ட உதவியாளர். விரிவான ஒப்பந்த சுருக்கம் வழங்கவும்.

ஒப்பந்த உரை:
\"\"\"{contract}\"\"\"

விரிவான சுருக்கம் வழங்கவும்:
1. முக்கிய தரப்பினர் மற்றும் அவர்களின் கடமைகள்
2. முக்கிய விதிமுறைகள் மற்றும் நிபந்தனைகள்
3. கட்டணம் மற்றும் விநியோக விதிமுறைகள்
4. ஆபத்து காரணிகள் மற்றும் சாத்தியமான பிரச்சினைகள்
5. முடிவு பிரிவுகள்
6. வணிக உரிமையாளருக்கான குறிப்பிட்ட பரிந்துரைகள்

தெளிவான, வணிக-நட்பு தமிழில் எழுதுங்கள்.
"""

def call_ai_model(prompt: str, model: str="gpt-4", system_message: str="You are a helpful legal assistant.", max_tokens: int=512) -> str:
  
    try:
        if model.startswith("gpt-"):
            # OpenAI models
            resp = openai_client.chat.completions.create(
                model=model,
                messages=[{"role":"system","content":system_message},
                          {"role":"user","content":prompt}],
                temperature=0.0,
                max_tokens=max_tokens,
                n=1
            )
            return resp.choices[0].message.content.strip()
        
        elif model.startswith("claude-3"):
            # Claude 3 models
            if not ANTHROPIC_API_KEY:
                raise Exception("Anthropic API key not configured")
            
            model_mapping = {
                "claude-3-sonnet": "claude-3-sonnet-20240229",
                "claude-3-haiku": "claude-3-haiku-20240307",
                "claude-3-opus": "claude-3-opus-20240229"
            }
            
            api_model = model_mapping.get(model, "claude-3-sonnet-20240229")
            
            response = anthropic_client.messages.create(
                model=api_model,
                max_tokens=max_tokens,
                temperature=0.0,
                system=system_message,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        
        elif model.startswith("gemini-"):
            # Gemini models
            if not GEMINI_API_KEY:
                raise Exception("Gemini API key not configured")
            
            model_mapping = {
                "gemini-2.0-flash": "gemini-2.0-flash-exp",
                "gemini-pro": "gemini-pro"
            }
            
            api_model = model_mapping.get(model, "gemini-2.0-flash-exp")
            gemini_model = genai.GenerativeModel(api_model)
            full_prompt = f"{system_message}\n\n{prompt}"
            response = gemini_model.generate_content(full_prompt)
            return response.text.strip()
        
        elif model.startswith("ollama-"):
            # Ollama models
            model_name = model.replace("ollama-", "")
            full_prompt = f"{system_message}\n\n{prompt}"
            
            response = ollama.chat(model=model_name, messages=[
                {'role': 'user', 'content': full_prompt}
            ])
            return response['message']['content'].strip()
        
        else:
            raise Exception(f"Unsupported model: {model}")
            
    except Exception as e:
        raise Exception(f"Error calling {model}: {str(e)}")

def call_gpt4_for_clause(clause: str, model: str="gpt-4", language: str="English", timeout: int=30) -> Dict:
    if language == "Hindi":
        prompt = CLAUSE_ANALYSIS_PROMPT_HINDI.format(clause=clause)
        system_message = "आप एक सहायक कानूनी सहायक हैं।"
    elif language == "Tamil":
        prompt = CLAUSE_ANALYSIS_PROMPT_TAMIL.format(clause=clause)
        system_message = "நீங்கள் ஒரு உதவிகரமான சட்ட உதவியாளர்."
    else:
        prompt = CLAUSE_ANALYSIS_PROMPT_ENGLISH.format(clause=clause)
        system_message = "You are a helpful legal assistant."
    
    try:
      
        text = call_ai_model(prompt, model, system_message, 1024)
        # parse JSON
        try:
            parsed = json.loads(text)
            if not parsed.get("explanation"):
                parsed["explanation"] = "Analysis not available"
            if not parsed.get("risk"):
                parsed["risk"] = "Medium"
            if not parsed.get("suggestion"):
                parsed["suggestion"] = "Please review with legal counsel"
        except Exception:
            parsed = {"explanation": text, "risk":"Medium", "suggestion": "Please review with legal counsel"}
        return parsed
    except Exception as e:
        return {"explanation": f"Error analyzing clause: {str(e)}", "risk":"Medium", "suggestion": "Please review manually"}

def call_gpt4_summary(contract_text: str, model: str="gpt-4", language: str="English") -> str:
    
    if language == "Hindi":
        prompt = SUMMARY_PROMPT_HINDI.format(contract=contract_text)
        system_message = "आप एक सहायक कानूनी सहायक हैं।"
    elif language == "Tamil":
        prompt = SUMMARY_PROMPT_TAMIL.format(contract=contract_text)
        system_message = "நீங்கள் ஒரு உதவிகரமான சட்ட உதவியாளர்."
    else:
        prompt = SUMMARY_PROMPT_ENGLISH.format(contract=contract_text)
        system_message = "You are a helpful legal assistant."
    
    try:
     
        return call_ai_model(prompt, model, system_message, 800)
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def ask_question_about_contract(question: str, contract_clauses: list, model: str="gpt-4", language: str="English") -> str:
   
    clauses_text = "\n\n".join([f"Clause {i+1}: {clause['clause']}" for i, clause in enumerate(contract_clauses)])
    
   
    if language == "Hindi":
        prompt = f"""आप भारतीय छोटे और मध्यम व्यापारियों के लिए एक कानूनी सहायक हैं। निम्नलिखित अनुबंध खंडों के आधार पर प्रश्न का उत्तर दें:

अनुबंध खंड:
{clauses_text}

प्रश्न: {question}

विस्तृत उत्तर दें जिसमें:
1. प्रश्न का सीधा उत्तर
2. संबंधित खंडों का संदर्भ
3. व्यापारिक सलाह
4. संभावित जोखिम या लाभ
5. संक्षिप्त और स्पष्ट सारांश

स्पष्ट हिंदी में उत्तर दें।"""
        system_message = "आप एक सहायक कानूनी सहायक हैं।"
    elif language == "Tamil":
        prompt = f"""நீங்கள் இந்திய சிறு மற்றும் நடுத்தர வணிகர்களுக்கான சட்ட உதவியாளர். பின்வரும் ஒப்பந்த பிரிவுகளின் அடிப்படையில் கேள்விக்கு பதிலளிக்கவும்:

ஒப்பந்த பிரிவுகள்:
{clauses_text}

கேள்வி: {question}

விரிவான பதில் வழங்கவும் :
1. கேள்விக்கு நேரடி பதில்
2. தொடர்புடைய பிரிவுகளின் குறிப்பு
3. வணிக ஆலோசனை
4. சாத்தியமான ஆபத்துகள் அல்லது நன்மைகள்
5. சுருக்கமான மற்றும் தெளிவான சுருக்கம்

தெளிவான தமிழில் பதிலளிக்கவும்."""
        system_message = "நீங்கள் ஒரு உதவிகரமான சட்ட உதவியாளர்."
    else:
        prompt = f"""You are a legal assistant for Indian SMEs. Answer the question based on the following contract clauses:

Contract Clauses:
{clauses_text}

Question: {question}

Provide a detailed answer including:
1. Direct answer to the question
2. Reference to relevant clauses
3. Business advice
4. Potential risks or benefits
5. Short and Crisp summary

Answer in clear, business-friendly English."""
        system_message = "You are a helpful legal assistant."
    
    try:
        return call_ai_model(prompt, model, system_message, 600)
    except Exception as e:
        return f"Error answering question: {str(e)}"
