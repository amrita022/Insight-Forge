export default function ChartPanel({ charts }) {
  if (!charts) {
    return null;
  }

  return (
    <div className="space-y-8">
      {/* Distribution Charts */}
      {charts.distributions && charts.distributions.length > 0 && (
        <div className="chart-section">
          <h3 className="chart-subsection-title">Distribution Analysis</h3>
          <div className="chart-grid">
            {charts.distributions.map((chart, index) => (
              <div key={index} className="chart-card">
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
          <h3 className="chart-subsection-title">Correlation Matrix</h3>
          <div className="chart-card w-full">
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
          <h3 className="chart-subsection-title">Outlier Detection (Box Plots)</h3>
          <div className="chart-grid">
            {charts.boxplots.map((chart, index) => (
              <div key={index} className="chart-card">
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
