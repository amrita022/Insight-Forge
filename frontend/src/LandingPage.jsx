import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, BarChart2, Brain, Zap, RefreshCw, FileText } from 'lucide-react';

export default function LandingPage() {
  const navigate = useNavigate();
  const howItWorksRef = useRef(null);

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

      /* NAVBAR */
      .navbar {
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
        transition: all 0.3s ease;
      }

      .navbar-logo {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 800;
        color: #1B6B5A;
        cursor: pointer;
        letter-spacing: -0.5px;
      }

      .navbar-links {
        display: flex;
        gap: 3rem;
        align-items: center;
      }

      .navbar-link {
        color: #2D2D2D;
        text-decoration: none;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: color 0.3s ease;
        position: relative;
      }

      .navbar-link:hover {
        color: #1B6B5A;
      }

      .navbar-link::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 0;
        height: 2px;
        background: #D4A853;
        transition: width 0.3s ease;
      }

      .navbar-link:hover::after {
        width: 100%;
      }

      .cta-btn {
        padding: 0.875rem 1.75rem;
        background: #1B6B5A;
        color: white;
        border: none;
        border-radius: 4px;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
      }

      .cta-btn:hover {
        background: #0f4935;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(27, 107, 90, 0.2);
      }

      /* HERO SECTION */
      .hero {
        padding: 6rem 4rem;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 3rem;
        align-items: center;
        position: relative;
        overflow: hidden;
      }

      .hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
          repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(27, 107, 90, 0.02) 2px, rgba(27, 107, 90, 0.02) 4px);
        pointer-events: none;
        opacity: 0.5;
      }

      .hero-content {
        z-index: 1;
      }

      .hero h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 1.5rem;
        color: #1B6B5A;
        letter-spacing: -1px;
      }

      .hero h1 .highlight {
        color: #D4A853;
      }

      .hero p {
        font-size: 1.125rem;
        color: #666;
        line-height: 1.6;
        margin-bottom: 2rem;
        max-width: 480px;
      }

      .hero-buttons {
        display: flex;
        gap: 1.5rem;
        align-items: center;
      }

      .btn-primary {
        padding: 1rem 2rem;
        background: #1B6B5A;
        color: white;
        border: none;
        border-radius: 4px;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
      }

      .btn-primary:hover {
        background: #0f4935;
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(27, 107, 90, 0.25);
      }

      .btn-secondary {
        padding: 1rem 2rem;
        background: transparent;
        color: #1B6B5A;
        border: 2px solid #1B6B5A;
        border-radius: 4px;
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
      }

      .btn-secondary:hover {
        background: #1B6B5A;
        color: white;
        transform: translateY(-2px);
      }

      .hero-visual {
        position: relative;
        z-index: 1;
      }

      .insight-mockup {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        animation: float 3s ease-in-out infinite;
      }

      @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
      }

      .insight-card {
        background: white;
        border: 1px solid rgba(27, 107, 90, 0.1);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(27, 107, 90, 0.08);
      }

      .insight-card h4 {
        font-size: 0.875rem;
        font-weight: 600;
        color: #1B6B5A;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .insight-card p {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1B6B5A;
      }

      .insight-card.secondary h4 {
        color: #D4A853;
      }

      .insight-card.secondary p {
        color: #D4A853;
      }

      /* FEATURES SECTION */
      .features {
        padding: 6rem 4rem;
      }

      .features h2 {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        color: #1B6B5A;
        margin-bottom: 4rem;
        text-align: center;
      }

      .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2.5rem;
      }

      .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        border: 1px solid rgba(27, 107, 90, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
      }

      .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 40px rgba(27, 107, 90, 0.12);
        border-color: #D4A853;
      }

      .feature-icon {
        width: 40px;
        height: 40px;
        margin-bottom: 1rem;
        color: #1B6B5A;
      }

      .feature-card h3 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1B6B5A;
        margin-bottom: 0.75rem;
      }

      .feature-card p {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.6;
      }

      /* HOW IT WORKS */
      .how-it-works {
        padding: 6rem 4rem;
        background: white;
        position: relative;
      }

      .how-it-works h2 {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        color: #1B6B5A;
        margin-bottom: 4rem;
        text-align: center;
      }

      .steps-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 3rem;
        position: relative;
      }

      .steps-container::before {
        content: '';
        position: absolute;
        top: 50px;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(to right, #1B6B5A 33%, transparent 33%, transparent 66%, #1B6B5A 66%);
      }

      .step {
        text-align: center;
        position: relative;
        z-index: 1;
      }

      .step-number {
        width: 60px;
        height: 60px;
        background: #1B6B5A;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 auto 1.5rem;
      }

      .step h3 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1B6B5A;
        margin-bottom: 0.75rem;
      }

      .step p {
        color: #666;
        font-size: 0.95rem;
      }

      /* CTA SECTION */
      .cta-section {
        padding: 5rem 4rem;
        background: white;
        border: 3px solid #1B6B5A;
        margin: 4rem;
        border-radius: 8px;
        text-align: center;
      }

      .cta-section h2 {
        font-family: 'Playfair Display', serif;
        font-size: 2.25rem;
        color: #1B6B5A;
        margin-bottom: 1rem;
      }

      .cta-section p {
        font-size: 1.125rem;
        color: #666;
        margin-bottom: 2.5rem;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
      }

      /* FOOTER */
      .footer {
        background: #1B6B5A;
        color: white;
        padding: 3rem 4rem 1.5rem;
      }

      .footer-content {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr;
        gap: 3rem;
        margin-bottom: 2rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      }

      .footer-brand h3 {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        color: #D4A853;
      }

      .footer-brand p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
      }

      .footer-column h4 {
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .footer-column a {
        display: block;
        color: rgba(255, 255, 255, 0.8);
        text-decoration: none;
        font-size: 0.9rem;
        margin-bottom: 0.75rem;
        transition: color 0.3s ease;
      }

      .footer-column a:hover {
        color: #D4A853;
      }

      .footer-bottom {
        text-align: center;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        padding: 1rem 0;
      }

      /* MOBILE RESPONSIVE */
      @media (max-width: 768px) {
        .navbar {
          padding: 1rem 1.5rem;
          flex-direction: column;
          gap: 1rem;
        }

        .navbar-links {
          flex-direction: column;
          gap: 1rem;
        }

        .hero {
          grid-template-columns: 1fr;
          padding: 3rem 1.5rem;
        }

        .hero h1 {
          font-size: 2.5rem;
        }

        .features-grid {
          grid-template-columns: 1fr;
        }

        .steps-container {
          grid-template-columns: 1fr;
        }

        .steps-container::before {
          display: none;
        }

        .footer-content {
          grid-template-columns: 1fr;
        }

        .cta-section {
          margin: 2rem 1.5rem;
          padding: 3rem 1.5rem;
        }
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
  }, []);

  const scrollToHowItWorks = () => {
    howItWorksRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div style={{ backgroundColor: '#FAF8F3', minHeight: '100vh' }}>
      {/* NAVBAR */}
      <nav className="navbar">
        <div className="navbar-logo" onClick={() => navigate('/')}>
          ⚡ Insight Forge
        </div>
        <div className="navbar-links">
          <a className="navbar-link" href="#features">Features</a>
          <a className="navbar-link" onClick={scrollToHowItWorks} style={{ cursor: 'pointer' }}>How It Works</a>
          <a className="navbar-link" href="#about">About</a>
          <button className="cta-btn" onClick={() => navigate('/app')}>Try It Free →</button>
        </div>
      </nav>

      {/* HERO SECTION */}
      <section className="hero">
        <div className="hero-content">
          <h1>
            Turn Raw Data Into<br />
            <span className="highlight">Actionable Intelligence</span>
          </h1>
          <p>
            Upload any CSV. Get AI-powered insights, visualizations, and business recommendations in seconds. No coding required.
          </p>
          <div className="hero-buttons">
            <button className="btn-primary" onClick={() => navigate('/app')}>
              Analyze Your Data →
            </button>
            <button className="btn-secondary" onClick={scrollToHowItWorks}>
              See How It Works
            </button>
          </div>
        </div>
        <div className="hero-visual">
          <div className="insight-mockup">
            <div className="insight-card">
              <h4>Key Trends</h4>
              <p>↗ +24%</p>
            </div>
            <div className="insight-card secondary">
              <h4>Anomalies</h4>
              <p>3</p>
            </div>
            <div className="insight-card secondary">
              <h4>Missing</h4>
              <p>0.2%</p>
            </div>
            <div className="insight-card">
              <h4>Correlation</h4>
              <p>0.87</p>
            </div>
          </div>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section className="features" id="features">
        <h2>Everything You Need to Understand Your Data</h2>
        <div className="features-grid">
          <div className="feature-card">
            <Search className="feature-icon" />
            <h3>Smart Preprocessing</h3>
            <p>Auto-detects missing values, outliers, and data types</p>
          </div>
          <div className="feature-card">
            <BarChart2 className="feature-icon" />
            <h3>Visual Charts</h3>
            <p>Distribution plots, correlation heatmaps, and box plots</p>
          </div>
          <div className="feature-card">
            <Brain className="feature-icon" />
            <h3>AI Insights</h3>
            <p>Gemini AI generates human-readable business insights</p>
          </div>
          <div className="feature-card">
            <Zap className="feature-icon" />
            <h3>Instant Results</h3>
            <p>Full analysis in under 30 seconds</p>
          </div>
          <div className="feature-card">
            <RefreshCw className="feature-icon" />
            <h3>Baseline Comparison</h3>
            <p>Compare AI analysis vs generic prompts</p>
          </div>
          <div className="feature-card">
            <FileText className="feature-icon" />
            <h3>Structured Output</h3>
            <p>Consistent, organized insights every time</p>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="how-it-works" id="how-it-works" ref={howItWorksRef}>
        <h2>Three Steps to Clarity</h2>
        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Upload</h3>
            <p>Drop your CSV file into Insight Forge</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>Analyze</h3>
            <p>Our AI preprocesses and analyzes your data</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Insights</h3>
            <p>Get actionable insights and visualizations</p>
          </div>
        </div>
      </section>

      {/* CTA SECTION */}
      <section className="cta-section" id="about">
        <h2>Ready to Unlock Your Data's Potential?</h2>
        <p>Join analysts and researchers using Insight Forge to make faster, smarter decisions</p>
        <button className="btn-primary" onClick={() => navigate('/app')}>
          Start Analyzing for Free →
        </button>
      </section>

      {/* FOOTER */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-brand">
            <h3>⚡ Insight Forge</h3>
            <p>Making data insights accessible to everyone</p>
          </div>
          <div className="footer-column">
            <h4>Product</h4>
            <a onClick={() => navigate('/app')} style={{ cursor: 'pointer' }}>Try the App</a>
            <a onClick={scrollToHowItWorks} style={{ cursor: 'pointer' }}>How It Works</a>
          </div>
          <div className="footer-column">
            <h4>Built With</h4>
            <a href="#">React</a>
            <a href="#">FastAPI</a>
            <a href="#">Gemini AI</a>
          </div>
        </div>
        <div className="footer-bottom">
          © 2025 Insight Forge.
        </div>
      </footer>
    </div>
  );
}
