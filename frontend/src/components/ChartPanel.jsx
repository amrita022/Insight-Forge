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

  const renderExplanation = (text) => {
    if (!text) return null;
    const paragraphs = text.split('\n\n');

    return (
      <div style={{ lineHeight: '1.6', fontSize: '0.9rem', color: '#333' }}>
        {paragraphs.map((para, idx) => {
          if (para.includes(':') && !para.includes('•')) {
            const parts = para.split(':');
            return (
              <div key={idx} style={{ marginBottom: '0.75rem' }}>
                <strong style={{ color: '#1B6B5A', display: 'block', marginBottom: '0.25rem' }}>
                  {parts[0]}:
                </strong>
                <span>{parts.slice(1).join(':')}</span>
              </div>
            );
          }

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

  const gridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
    gap: '1.5rem',
  };

  const hoverOn = (e) => {
    e.currentTarget.style.boxShadow = '0 4px 12px rgba(27, 107, 90, 0.1)';
    e.currentTarget.style.transform = 'translateY(-2px)';
  };

  const hoverOff = (e) => {
    e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
    e.currentTarget.style.transform = 'translateY(0)';
  };

  const renderCard = (title, image, expKey) => (
    <div
      style={chartCardStyle}
      onMouseEnter={hoverOn}
      onMouseLeave={hoverOff}
    >
      {title && (
        <p style={{
          fontSize: '0.875rem',
          fontWeight: '700',
          color: '#1B6B5A',
          marginBottom: '1rem',
          fontFamily: '"DM Sans", sans-serif',
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
        }}>
          {title}
        </p>
      )}

      <img
        src={`data:image/png;base64,${image}`}
        style={{ width: '100%', borderRadius: '8px', marginBottom: '1rem' }}
      />

      {explanations[expKey] && (
        <div style={{
          background: '#F5FBF9',
          border: '1px solid #D4E8E3',
          borderRadius: '8px',
          padding: '1rem',
        }}>
          <h4 style={{
            fontSize: '0.875rem',
            fontWeight: '600',
            color: '#1B6B5A',
            marginBottom: '0.75rem',
          }}>
            📖 What This Shows
          </h4>
          {renderExplanation(explanations[expKey])}
        </div>
      )}
    </div>
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

      {/* EXISTING SECTIONS (unchanged) */}
      {charts.distributions && (
        <div>
          <h3 style={sectionTitleStyle}>📊 Distribution Analysis</h3>
          <div style={gridStyle}>
            {charts.distributions.map((c, i) =>
              renderCard(c.column, c.image, `distribution_${c.column}`)
            )}
          </div>
        </div>
      )}

      {/* ✅ NEW: KDE */}
      {charts.kde_plots && (
        <div>
          <h3 style={sectionTitleStyle}>〰️ KDE Density Curves</h3>
          <div style={gridStyle}>
            {charts.kde_plots.map((c, i) =>
              renderCard(c.column, c.image, `kde_${c.column}`)
            )}
          </div>
        </div>
      )}

      {/* ✅ NEW: Scatter */}
      {charts.scatter_plots && (
        <div>
          <h3 style={sectionTitleStyle}>🔵 Scatter Relationships</h3>
          <div style={gridStyle}>
            {charts.scatter_plots.map((c, i) =>
              renderCard(`${c.x_column} vs ${c.y_column}`, c.image, `scatter_${c.x_column}_vs_${c.y_column}`)
            )}
          </div>
        </div>
      )}

      {/* ✅ NEW: Line Charts */}
      {charts.line_charts && (
        <div>
          <h3 style={sectionTitleStyle}>📈 Line Trends</h3>
          <div style={gridStyle}>
            {charts.line_charts.map((c, i) =>
              renderCard(c.column, c.image, `line_${c.column}`)
            )}
          </div>
        </div>
      )}

      {/* EXISTING */}
      {charts.boxplots && (
        <div>
          <h3 style={sectionTitleStyle}>📦 Box Plots</h3>
          <div style={gridStyle}>
            {charts.boxplots.map((c, i) =>
              renderCard(c.column, c.image, `boxplot_${c.column}`)
            )}
          </div>
        </div>
      )}

      {/* ✅ NEW: Violin */}
      {charts.violin_plots && (
        <div>
          <h3 style={sectionTitleStyle}>🎻 Violin Plots</h3>
          <div style={gridStyle}>
            {charts.violin_plots.map((c, i) =>
              renderCard(c.column, c.image, `violin_${c.column}`)
            )}
          </div>
        </div>
      )}

      {/* EXISTING */}
      {charts.correlation && (
        <div>
          <h3 style={sectionTitleStyle}>🔗 Correlation Matrix</h3>
          {renderCard(null, charts.correlation, 'correlation_heatmap')}
        </div>
      )}

      {/* ✅ NEW: Pair Plot */}
      {charts.pair_plot && (
        <div>
          <h3 style={sectionTitleStyle}>🔢 Pair Plot</h3>
          {renderCard(null, charts.pair_plot.image, 'pair_plot')}
        </div>
      )}

      {/* ✅ NEW: Bubble */}
      {charts.bubble_charts && (
        <div>
          <h3 style={sectionTitleStyle}>🫧 Bubble Charts</h3>
          <div style={gridStyle}>
            {charts.bubble_charts.map((c, i) =>
              renderCard(`${c.x_column} vs ${c.y_column}`, c.image, `bubble_${c.x_column}_vs_${c.y_column}`)
            )}
          </div>
        </div>
      )}

      {/* ✅ NEW: Pie */}
      {charts.pie_charts && (
        <div>
          <h3 style={sectionTitleStyle}>🥧 Pie Charts</h3>
          <div style={gridStyle}>
            {charts.pie_charts.map((c, i) =>
              renderCard(c.column, c.image, `pie_${c.column}`)
            )}
          </div>
        </div>
      )}

      {/* EXISTING */}
      {charts.missing_data_heatmap && (
        <div>
          <h3 style={sectionTitleStyle}>❌ Missing Data</h3>
          {renderCard(null, charts.missing_data_heatmap, 'missing_data')}
        </div>
      )}

      {charts.numeric_summary_stats && (
        <div>
          <h3 style={sectionTitleStyle}>📉 Summary Statistics</h3>
          {renderCard(null, charts.numeric_summary_stats, 'summary_dashboard')}
        </div>
      )}
    </div>
  );
}