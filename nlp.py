import fitz
import docx
import re
import spacy
from typing import List
import nltk


nltk.download("punkt")


nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path: str) -> str:

    doc = fitz.open(file_path)
    text_chunks = []
    for page in doc:
        text_chunks.append(page.get_text())
    return "\n".join(text_chunks)
    

def extract_text_from_docx(file_path: str) -> str:

    doc = docx.Document(file_path)
    text_chunks = [para.text for para in doc.paragraphs]
    return "\n".join(text_chunks)

def clean_text(text: str) -> str:

    text = re.sub(r'\s+', ' ', text) 
    text = re.sub(r'\n+', '\n', text)  
    return text.strip()

def split_into_clauses(text: str, max_clause_len: int = 800) -> List[str]:

    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    clauses = []
    current = ""
    for s in sentences:
        if len(current) + len(s) < max_clause_len:
            current = (current + " " + s).strip()
        else:
            clauses.append(current)
            current = s
    if current:
        clauses.append(current)

    final = []
    for c in clauses:
        parts = re.split(r'(?:\n|(?<=\.)\s{2,}|(?:\d+\.) )', c)
        parts = [p.strip() for p in parts if p and len(p.strip())>10]
        final.extend(parts)
    return final



