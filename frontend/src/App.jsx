import { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import LandingPage from './LandingPage';
import UploadZone from './components/UploadZone';
import InsightCard from './components/InsightCard';
import ChartPanel from './components/ChartPanel';
import StatsTable from './components/StatsTable';

function AnalysisApp() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState(null);

  useEffect(() => {
    // Inject Google Fonts
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@400;500;600;700&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);

    // Inject CSS Styles
    const style = document.createElement('style');
    style.textContent = `
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: 'DM Sans', sans-serif;
        background-color: #FAF8F3;
        color: #2D2D2D;
        overflow-x: hidden;
      }

      html {
        scroll-behavior: smooth;
      }

      .app-container {
        min-height: 100vh;
        background-color: #FAF8F3;
      }

      /* NAVBAR */
      .app-navbar {
        position: sticky;
        top: 0;
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 4rem;
        background: rgba(250, 248, 243, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(27, 107, 90, 0.1);
      }

      .app-navbar-logo {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: #1B6B5A;
        cursor: pointer;
        letter-spacing: -0.5px;
      }

      .app-navbar-logo:hover {
        opacity: 0.8;
      }

      /* MAIN CONTENT */
      .app-main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 3rem 2rem;
      }

      /* UPLOAD CARD */
      .upload-card {
        background: white;
        border: 1px solid #E8E4DC;
        border-radius: 12px;
        padding: 3rem;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 2px 8px rgba(27, 107, 90, 0.05);
      }

      .upload-card h2 {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: #1B6B5A;
        margin-bottom: 0.5rem;
        text-align: center;
      }

      .upload-card .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1rem;
      }

      /* LOADING STATE */
      .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 4rem 2rem;
        gap: 1rem;
      }

      .spinner {
        width: 48px;
        height: 48px;
        border: 4px solid #E8E4DC;
        border-top: 4px solid #1B6B5A;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      }

      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }

      .loading-text {
        color: #1B6B5A;
        font-size: 1rem;
        font-weight: 500;
      }

      /* ERROR STATE */
      .error-card {
        background: #FEE;
        border: 1px solid #F99;
        border-left: 4px solid #D32F2F;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-bottom: 2rem;
        color: #C62828;
        font-size: 0.95rem;
      }

      /* RESULTS CONTAINER */
      .results-container {
        space-y: 2rem;
      }

      .mode-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 24px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 2rem;
      }

      .mode-badge.structured {
        background: #E3F2FD;
        color: #1B6B5A;
      }

      .mode-badge.baseline {
        background: #F5F5F5;
        color: #666;
      }

      /* INSIGHTS GRID */
      .insights-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
      }

      /* RESET BUTTON */
      .reset-button-container {
        display: flex;
        justify-content: center;
        margin-top: 3rem;
        padding-top: 2rem;
      }

      .btn-reset {
        padding: 0.875rem 2rem;
        background: white;
        color: #1B6B5A;
        border: 2px solid #1B6B5A;
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
      }

      .btn-reset:hover {
        background: #1B6B5A;
        color: white;
        transform: translateY(-2px);
      }

      /* CHARTS AND STATS */
      .stats-container {
        margin: 2rem 0;
      }

      .charts-container {
        margin: 2rem 0;
      }

      /* MOBILE */
      @media (max-width: 768px) {
        .app-navbar {
          padding: 1rem 1.5rem;
        }

        .app-main {
          padding: 1.5rem 1rem;
        }

        .upload-card {
          padding: 1.5rem;
        }

        .upload-card h2 {
          font-size: 1.5rem;
        }

        .insights-grid {
          grid-template-columns: 1fr;
        }
      }
    `;
    document.head.appendChild(style);

    return () => {
      try {
        document.head.removeChild(style);
      } catch (e) {}
    };
  }, []);

  const API_BASE = 'https://insight-forge-production-0b14.up.railway.app';

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
    <div className="app-container">
      {/* NAVBAR */}
      <nav className="app-navbar">
        <div className="app-navbar-logo" onClick={() => navigate('/')}>
          ⚡ Insight Forge
        </div>
      </nav>

      {/* MAIN CONTENT */}
      <main className="app-main">
        {!results ? (
          <>
            {/* Upload State */}
            {!loading && (
              <div className="upload-card">
                <h2>Analyze Your Dataset</h2>
                <p className="subtitle">Upload a CSV file to get AI-powered insights</p>
                <UploadZone
                  onAnalyze={handleAnalyze}
                  onBaseline={handleBaseline}
                  file={file}
                  isLoading={loading}
                  onFileSelect={handleFileSelect}
                />
              </div>
            )}

            {/* Loading State */}
            {loading && (
              <div className="loading-container">
                <div className="spinner"></div>
                <p className="loading-text">Analyzing your dataset...</p>
              </div>
            )}

            {/* Error State */}
            {error && <div className="error-card">{error}</div>}
          </>
        ) : (
          <>
            {/* Results State */}
            <div className="results-container">
              {/* Mode Badge */}
              <div className={`mode-badge ${mode === 'baseline' ? 'baseline' : 'structured'}`}>
                {mode === 'baseline' ? 'Baseline Analysis' : 'Structured Analysis'}
              </div>

              {/* Stats Cards */}
              {results.stats && (
                <div className="stats-container">
                  <StatsTable stats={results.stats} />
                </div>
              )}

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
              {results.charts && (
                <div className="charts-container">
                  <ChartPanel charts={results.charts} />
                </div>
              )}

              {/* Reset Button */}
              <div className="reset-button-container">
                <button onClick={handleReset} className="btn-reset">
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

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/app" element={<AnalysisApp />} />
    </Routes>
  );
}
