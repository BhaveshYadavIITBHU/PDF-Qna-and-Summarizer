import React, { useState } from 'react';
import './Home.css';

function Home() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [pdfText, setPdfText] = useState('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');

      const data = await response.json();
      setSummary(data.summary);
      setPdfText(data.text);
      setProgress(100);
    } catch (error) {
      console.error('Error:', error);
      alert('Error uploading PDF');
    } finally {
      setLoading(false);
    }
  };

  const handleQuestion = async (e) => {
    e.preventDefault();
    if (!question || !pdfText) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/ask-question', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question,
          pdf_text: pdfText,
        }),
      });

      if (!response.ok) throw new Error('Question failed');

      const data = await response.json();
      setAnswer(data.answer);
      setConfidence(data.confidence);
    } catch (error) {
      console.error('Error:', error);
      alert('Error getting answer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home">
      <div className="upload-section">
        <h2>Upload PDF</h2>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={!file || loading}>
          Upload and Process
        </button>
        
        {loading && (
          <div className="progress-container">
            <div className="progress-bar" style={{ width: `${progress}%` }}></div>
          </div>
        )}

        {summary && (
          <div className="summary-section">
            <h3>Summary</h3>
            <p>{summary}</p>
          </div>
        )}
      </div>

      {pdfText && (
        <div className="qa-section">
          <h2>Ask Questions</h2>
          <form onSubmit={handleQuestion}>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Enter your question..."
              disabled={loading}
            />
            <button type="submit" disabled={loading}>
              Ask
            </button>
          </form>

          {answer && (
            <div className="answer-section">
              <h3>Answer</h3>
              <p>{answer}</p>
              {confidence && (
                <p className="confidence">
                  Confidence: {confidence.toFixed(1)}%
                </p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Home; 