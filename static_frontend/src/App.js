import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!query.trim()) {
      setError('Please enter a query.');
      return;
    }
    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/rag_query/', { question: query });
      setResult(response.data);
    } catch (err) {
      console.error("Error fetching RAG query:", err);
      let errorMessage = 'Failed to fetch data. Ensure the backend is running.';
      if (err.response) {
        errorMessage = err.response.data?.detail || `Server error: ${err.response.status}`;
      } else if (err.request) {
        errorMessage = 'No response from server. Is it running?';
      }
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>News Article RAG Query</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit} className="query-form">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your query here..."
            rows="3"
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Processing...' : 'Submit Query'}
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}

        {isLoading && <p>Loading results...</p>}

        {result && (
          <div className="results-container">
            <h2>Query Results</h2>

            <div className="result-section">
              <h3>Response:</h3>
              <p>{result.response}</p>
            </div>

            <div className="result-section">
              <h3>Context Used:</h3>
              <p className="context-text">{result.context}</p>
            </div>

            <div className="result-section">
              <h3>Evaluation Metrics:</h3>
              <div className="metrics">
                <p><strong>Context Relevance:</strong> {result.evaluation_metrics.context_relevance.toFixed(2)}</p>
                {result.evaluation_metrics.context_relevance_reasoning && <p className="reasoning"><em>Reasoning: {result.evaluation_metrics.context_relevance_reasoning}</em></p>}

                <p><strong>Faithfulness:</strong> {result.evaluation_metrics.faithfulness.toFixed(2)}</p>
                {result.evaluation_metrics.faithfulness_reasoning && <p className="reasoning"><em>Reasoning: {result.evaluation_metrics.faithfulness_reasoning}</em></p>}
                
                <p><strong>Answer Relevance to Query:</strong> {result.evaluation_metrics.answer_relevance_q.toFixed(2)}</p>
                {result.evaluation_metrics.answer_relevance_q_reasoning && <p className="reasoning"><em>Reasoning: {result.evaluation_metrics.answer_relevance_q_reasoning}</em></p>}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;