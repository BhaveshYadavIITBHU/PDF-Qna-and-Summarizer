# PDF Summarizer & Q&A

A stylish web application that allows you to upload PDF files, get automatic summaries, and ask questions about the content using AI.

## Features

- PDF text extraction
- Automatic text summarization using BART model
- Question answering using RoBERTa model
- Progress bars and loading indicators
- Modern and responsive UI
- Confidence scores for answers

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

3. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Usage

1. Upload a PDF file using the file uploader
2. Wait for the summary to be generated
3. Read the summary of the PDF content
4. Ask questions about the PDF content in the question input field
5. Get answers with confidence scores

## Technical Details

- Uses Streamlit for the web interface
- PyPDF2 for PDF text extraction
- Hugging Face Transformers for summarization and question answering
- Sentence Transformers for semantic search
- Custom CSS for styling

## Note

The first time you run the application, it will download the required AI models, which might take a few minutes depending on your internet connection. 