export default function ChartPanel({ charts, explanations = {} }) {
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
    padding: '1.5rem',
    border: '1px solid #E8E4DC',
    boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
    transition: 'all 0.3s ease',
    cursor: 'default',
  };

  // Helper function to render explanations with formatting
  const renderExplanation = (text) => {
    if (!text) return null;
    
    // Split text into paragraphs and format key sections
    const paragraphs = text.split('\n\n');
    return (
      <div style={{ lineHeight: '1.6', fontSize: '0.9rem', color: '#333' }}>
        {paragraphs.map((para, idx) => {
          // Check if this is a bold section header
          if (para.includes(':') && !para.includes('•')) {
            const parts = para.split(':');
            return (
              <div key={idx} style={{ marginBottom: '0.75rem' }}>
                <strong style={{ color: '#1B6B5A', display: 'block', marginBottom: '0.25rem' }}>
                  {parts[0]}:
                </strong>
                <span>{parts[1]}</span>
              </div>
            );
          }
          
          // Format bullet points
          if (para.includes('•')) {
            return (
              <div key={idx} style={{ marginBottom: '0.75rem' }}>
                {para.split('\n').map((line, lineIdx) => (
                  <div key={lineIdx} style={{ marginBottom: '0.25rem' }}>
                    {line}
                  </div>
                ))}
              </div>
            );
          }

          return (
            <p key={idx} style={{ marginBottom: '0.75rem' }}>
              {para}
            </p>
          );
        })}
      </div>
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Distribution Charts */}
      {charts.distributions && charts.distributions.length > 0 && (
        <div>
          <h3 style={sectionTitleStyle}>📊 Distribution Analysis</h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: '1.5rem',
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
                  fontWeight: '700',
                  color: '#1B6B5A',
                  marginBottom: '1rem',
                  fontFamily: '"DM Sans", sans-serif',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                }}>
                  {chart.column}
                </p>
                <img
                  src={`data:image/png;base64,${chart.image}`}
                  alt={`Distribution of ${chart.column}`}
                  style={{ 
                    width: '100%', 
                    height: 'auto', 
                    borderRadius: '8px',
                    marginBottom: '1rem'
                  }}
                />

                {/* Chart Explanation (NEW) */}
                {explanations[`distribution_${chart.column}`] && (
                  <div style={{
                    background: '#F5FBF9',
                    border: '1px solid #D4E8E3',
                    borderRadius: '8px',
                    padding: '1rem',
                    marginTop: '0.75rem',
                  }}>
                    <h4 style={{
                      fontSize: '0.875rem',
                      fontWeight: '600',
                      color: '#1B6B5A',
                      marginBottom: '0.75rem',
                      fontFamily: '"DM Sans", sans-serif',
                    }}>
                      📖 What This Shows
                    </h4>
                    {renderExplanation(explanations[`distribution_${chart.column}`])}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Correlation Heatmap */}
      {charts.correlation && (
        <div>
          <h3 style={sectionTitleStyle}>🔗 Correlation Matrix</h3>
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
              style={{ 
                width: '100%', 
                height: 'auto', 
                borderRadius: '8px',
                marginBottom: '1rem'
              }}
            />

            {/* Correlation Explanation (NEW) */}
            {explanations['correlation_heatmap'] && (
              <div style={{
                background: '#F5FBF9',
                border: '1px solid #D4E8E3',
                borderRadius: '8px',
                padding: '1rem',
                marginTop: '0.75rem',
              }}>
                <h4 style={{
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#1B6B5A',
                  marginBottom: '0.75rem',
                  fontFamily: '"DM Sans", sans-serif',
                }}>
                  📖 What This Shows
                </h4>
                {renderExplanation(explanations['correlation_heatmap'])}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Box Plots */}
      {charts.boxplots && charts.boxplots.length > 0 && (
        <div>
          <h3 style={sectionTitleStyle}>📦 Outlier Detection (Box Plots)</h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: '1.5rem',
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
                  fontWeight: '700',
                  color: '#1B6B5A',
                  marginBottom: '1rem',
                  fontFamily: '"DM Sans", sans-serif',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                }}>
                  {chart.column}
                </p>
                <img
                  src={`data:image/png;base64,${chart.image}`}
                  alt={`Box plot of ${chart.column}`}
                  style={{ 
                    width: '100%', 
                    height: 'auto', 
                    borderRadius: '8px',
                    marginBottom: '1rem'
                  }}
                />

                {/* Boxplot Explanation (NEW) */}
                {explanations[`boxplot_${chart.column}`] && (
                  <div style={{
                    background: '#F5FBF9',
                    border: '1px solid #D4E8E3',
                    borderRadius: '8px',
                    padding: '1rem',
                    marginTop: '0.75rem',
                  }}>
                    <h4 style={{
                      fontSize: '0.875rem',
                      fontWeight: '600',
                      color: '#1B6B5A',
                      marginBottom: '0.75rem',
                      fontFamily: '"DM Sans", sans-serif',
                    }}>
                      📖 What This Shows
                    </h4>
                    {renderExplanation(explanations[`boxplot_${chart.column}`])}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Missing Data Visualization (NEW) */}
      {charts.missing_data_heatmap && (
        <div>
          <h3 style={sectionTitleStyle}>❌ Missing Data Analysis</h3>
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
              src={`data:image/png;base64,${charts.missing_data_heatmap}`}
              alt="Missing Data Visualization"
              style={{ 
                width: '100%', 
                height: 'auto', 
                borderRadius: '8px',
                marginBottom: '1rem'
              }}
            />

            {/* Missing Data Explanation (NEW) */}
            {explanations['missing_data'] && (
              <div style={{
                background: '#F5FBF9',
                border: '1px solid #D4E8E3',
                borderRadius: '8px',
                padding: '1rem',
                marginTop: '0.75rem',
              }}>
                <h4 style={{
                  fontSize: '0.875rem',
                  fontWeight: '600',
                  color: '#1B6B5A',
                  marginBottom: '0.75rem',
                  fontFamily: '"DM Sans", sans-serif',
                }}>
                  📖 What This Shows
                </h4>
                {renderExplanation(explanations['missing_data'])}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Categorical Distributions (NEW) */}
      {charts.categorical_distributions && charts.categorical_distributions.length > 0 && (
        <div>
          <h3 style={sectionTitleStyle}>🏷️ Categorical Analysis</h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: '1.5rem',
          }}>
            {charts.categorical_distributions.map((chart, index) => (
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
                  fontWeight: '700',
                  color: '#1B6B5A',
                  marginBottom: '1rem',
                  fontFamily: '"DM Sans", sans-serif',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                }}>
                  {chart.column}
                </p>
                <img
                  src={`data:image/png;base64,${chart.image}`}
                  alt={`Categories in ${chart.column}`}
                  style={{ 
                    width: '100%', 
                    height: 'auto', 
                    borderRadius: '8px',
                    marginBottom: '1rem'
                  }}
                />

                {/* Categorical Explanation (NEW) */}
                {explanations[`categorical_${chart.column}`] && (
                  <div style={{
                    background: '#F5FBF9',
                    border: '1px solid #D4E8E3',
                    borderRadius: '8px',
                    padding: '1rem',
                    marginTop: '0.75rem',
                  }}>
                    <h4 style={{
                      fontSize: '0.875rem',
                      fontWeight: '600',
                      color: '#1B6B5A',
                      marginBottom: '0.75rem',
                      fontFamily: '"DM Sans", sans-serif',
                    }}>
                      📖 What This Shows
                    </h4>
                    {renderExplanation(explanations[`categorical_${chart.column}`])}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Summary Statistics Dashboard (NEW) */}
      {charts.numeric_summary_stats && (
        <div>
          <h3 style={sectionTitleStyle}>📈 Summary Statistics</h3>
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
              src={`data:image/png;base64,${charts.numeric_summary_stats}`}
              alt="Summary Statistics"
              style={{ 
                width: '100%', 
                height: 'auto', 
                borderRadius: '8px'
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}