from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import torch
from transformers import pipeline  # ✅ Only this needed from transformers

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Optional
from pydantic import BaseModel
import io

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def split_text_into_chunks(text, chunk_size=1000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        current_chunk.append(word)
        current_size += len(word) + 1
        if current_size >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

class Question(BaseModel):
    question: str
    pdf_text: str

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        
        # Extract text
        text = extract_text_from_pdf(pdf_file)
        
        # Split into chunks
        chunks = split_text_into_chunks(text)
        
        # Generate summary
        summaries = []
        for chunk in chunks:
            if len(chunk.split()) > 100:
                summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                summaries.append(summary[0]['summary_text'])
        
        final_summary = " ".join(summaries)
        
        return {
            "summary": final_summary,
            "text": text,
            "chunks": chunks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask-question")
async def ask_question(question_data: Question):
    try:
        chunks = split_text_into_chunks(question_data.pdf_text)
        
        # Find most relevant chunk
        question_embedding = sentence_model.encode(question_data.question)
        chunk_embeddings = [sentence_model.encode(chunk) for chunk in chunks]
        
        similarities = [np.dot(question_embedding, chunk_embedding) / 
                       (np.linalg.norm(question_embedding) * np.linalg.norm(chunk_embedding))
                       for chunk_embedding in chunk_embeddings]
        
        most_relevant_chunk = chunks[np.argmax(similarities)]
        
        # Get answer
        answer = qa_model(question=question_data.question, context=most_relevant_chunk)
        
        return {
            "answer": answer['answer'],
            "confidence": float(answer['score'] * 100)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 