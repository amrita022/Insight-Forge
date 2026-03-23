export default function ChartPanel({ charts }) {
  if (!charts) {
    return null;
  }

  const sectionTitleStyle = {
    fontSize: '1.5rem',
    fontWeight: '700',
    color: '#1B6B5A',
    marginBottom: '1.5rem',
    fontFamily: '"Playfair Display", serif',
  };

  const chartCardStyle = {
    background: 'white',
    borderRadius: '12px',
    padding: '1rem',
    border: '1px solid #E8E4DC',
    boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
    transition: 'all 0.3s ease',
    cursor: 'default',
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Distribution Charts */}
      {charts.distributions && charts.distributions.length > 0 && (
        <div>
          <h3 style={sectionTitleStyle}>Distribution Analysis</h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '1rem',
          }}>
            {charts.distributions.map((chart, index) => (
              <div
                key={index}
                style={chartCardStyle}
                onMouseEnter={(e) => {
                  e.currentTarget.style.boxShadow = '0 4px 12px rgba(27, 107, 90, 0.1)';
                  e.currentTarget.style.transform = 'translateY(-2px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                <p style={{
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#1B6B5A',
                  marginBottom: '0.75rem',
                  fontFamily: '"DM Sans", sans-serif',
                }}>
                  {chart.column}
                </p>
                <img
                  src={`data:image/png;base64,${chart.image}`}
                  alt={`Distribution of ${chart.column}`}
                  style={{ width: '100%', height: 'auto', borderRadius: '8px' }}
                />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Correlation Heatmap */}
      {charts.correlation && (
        <div>
          <h3 style={sectionTitleStyle}>Correlation Matrix</h3>
          <div style={chartCardStyle}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(27, 107, 90, 0.1)';
              e.currentTarget.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
              e.currentTarget.style.transform = 'translateY(0)';
            }}>
            <img
              src={`data:image/png;base64,${charts.correlation}`}
              alt="Correlation Matrix"
              style={{ width: '100%', height: 'auto', borderRadius: '8px' }}
            />
          </div>
        </div>
      )}

      {/* Box Plots */}
      {charts.boxplots && charts.boxplots.length > 0 && (
        <div>
          <h3 style={sectionTitleStyle}>Outlier Detection (Box Plots)</h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '1rem',
          }}>
            {charts.boxplots.map((chart, index) => (
              <div
                key={index}
                style={chartCardStyle}
                onMouseEnter={(e) => {
                  e.currentTarget.style.boxShadow = '0 4px 12px rgba(27, 107, 90, 0.1)';
                  e.currentTarget.style.transform = 'translateY(-2px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
                  e.currentTarget.style.transform = 'translateY(0)';
                }}
              >
                <p style={{
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#1B6B5A',
                  marginBottom: '0.75rem',
                  fontFamily: '"DM Sans", sans-serif',
                }}>
                  {chart.column}
                </p>
                <img
                  src={`data:image/png;base64,${chart.image}`}
                  alt={`Box plot of ${chart.column}`}
                  style={{ width: '100%', height: 'auto', borderRadius: '8px' }}
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
