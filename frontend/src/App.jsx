import { useState } from 'react';
import './App.css';
import UploadZone from './components/UploadZone';
import InsightCard from './components/InsightCard';
import ChartPanel from './components/ChartPanel';
import StatsTable from './components/StatsTable';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState(null);

  const API_BASE = 'http://localhost:8000';

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
  };

  const sendAnalysisRequest = async (endpoint) => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP Error: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
      setMode(endpoint === '/analyze/baseline' ? 'baseline' : 'structured');
    } catch (err) {
      setError(`Analysis failed: ${err.message}`);
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = () => {
    sendAnalysisRequest('/analyze');
  };

  const handleBaseline = () => {
    sendAnalysisRequest('/analyze/baseline');
  };

  const handleReset = () => {
    setFile(null);
    setResults(null);
    setError(null);
    setMode(null);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">Insight Forge</h1>
          <p className="app-subtitle">AI-Powered Exploratory Data Analysis</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        {!results ? (
          <>
            {/* Upload State */}
            <UploadZone
              onAnalyze={handleAnalyze}
              onBaseline={handleBaseline}
              file={file}
              isLoading={loading}
              onFileSelect={handleFileSelect}
            />

            {/* Loading State */}
            {loading && (
              <div className="loading-state">
                <div className="spinner"></div>
                <p className="loading-text">Analyzing your dataset...</p>
              </div>
            )}

            {/* Error State */}
            {error && <div className="error-message">{error}</div>}
          </>
        ) : (
          <>
            {/* Results State */}
            <div className="results-container">
              {/* Mode Badge */}
              <div className="mode-badge">
                {mode === 'baseline' ? 'Baseline Analysis' : 'Structured Analysis'}
              </div>

              {/* Stats Table */}
              {results.stats && <StatsTable stats={results.stats} />}

              {/* Insight Cards */}
              {results.insights && (
                <div className="insights-grid">
                  {results.insights.summary && (
                    <InsightCard title="Summary" items={results.insights.summary} />
                  )}
                  {results.insights.key_trends && (
                    <InsightCard title="Key Trends" items={results.insights.key_trends} />
                  )}
                  {results.insights.outliers && (
                    <InsightCard title="Outliers" items={results.insights.outliers} />
                  )}
                  {results.insights.correlations && (
                    <InsightCard title="Correlations" items={results.insights.correlations} />
                  )}
                  {results.insights.missing_data_notes && (
                    <InsightCard title="Missing Data" items={results.insights.missing_data_notes} />
                  )}
                  {results.insights.business_insights && (
                    <InsightCard title="Business Insights" items={results.insights.business_insights} />
                  )}
                  {results.insights.recommended_next_steps && (
                    <InsightCard
                      title="Recommended Next Steps"
                      items={results.insights.recommended_next_steps}
                    />
                  )}
                </div>
              )}

              {/* Charts */}
              {results.charts && <ChartPanel charts={results.charts} />}

              {/* Reset Button */}
              <div className="reset-button-container">
                <button onClick={handleReset} className="btn btn-reset">
                  Analyze Another Dataset
                </button>
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
