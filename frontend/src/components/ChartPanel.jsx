import '../styles/ChartPanel.css';

export default function ChartPanel({ charts }) {
  if (!charts) {
    return null;
  }

  return (
    <div className="chart-panel">
      {/* Distribution Charts */}
      {charts.distributions && charts.distributions.length > 0 && (
        <div className="chart-section">
          <h3 className="section-title">Distribution Analysis</h3>
          <div className="chart-grid">
            {charts.distributions.map((chart, index) => (
              <div key={index} className="chart-item">
                <p className="chart-label">{chart.column}</p>
                <img
                  src={`data:image/png;base64,${chart.image}`}
                  alt={`Distribution of ${chart.column}`}
                  className="chart-image"
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Correlation Heatmap */}
      {charts.correlation && (
        <div className="chart-section">
          <h3 className="section-title">Correlation Matrix</h3>
          <div className="chart-item full-width">
            <img
              src={`data:image/png;base64,${charts.correlation}`}
              alt="Correlation Matrix"
              className="chart-image"
            />
          </div>
        </div>
      )}

      {/* Box Plots */}
      {charts.boxplots && charts.boxplots.length > 0 && (
        <div className="chart-section">
          <h3 className="section-title">Outlier Detection (Box Plots)</h3>
          <div className="chart-grid">
            {charts.boxplots.map((chart, index) => (
              <div key={index} className="chart-item">
                <p className="chart-label">{chart.column}</p>
                <img
                  src={`data:image/png;base64,${chart.image}`}
                  alt={`Box plot of ${chart.column}`}
                  className="chart-image"
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
