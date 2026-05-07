export default function ChartPanel({ charts, stats, mode }) {
  if (!charts) {
    return null;
  }

  const isBaseline = mode === 'baseline' || stats?.analysis_depth === 'baseline';

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

  const explanationStyle = {
    fontSize: '0.9rem',
    color: '#555',
    marginTop: '1rem',
    paddingTop: '1rem',
    borderTop: '1px solid #E8E4DC',
    lineHeight: '1.5',
    fontStyle: 'italic',
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
                {/* Distribution Explanation */}
                {isBaseline ? (
                  <p style={explanationStyle}>
                    This chart shows how values for {chart.column} are spread out. Taller bars mean more records in that range, so you can quickly spot the common range and whether the data is tightly packed or widely spread.
                  </p>
                ) : stats?.distribution_explanations?.[chart.column]?.layman_narrative ? (
                  <p style={explanationStyle}>
                    {stats.distribution_explanations[chart.column].layman_narrative}
                  </p>
                ) : stats?.distribution_explanations?.[chart.column]?.narrative ? (
                  <p style={explanationStyle}>
                    {stats.distribution_explanations[chart.column].narrative}
                  </p>
                ) : null}
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
            {/* Correlation Explanation (plain summary if available) */}
            {isBaseline ? (
              <p style={explanationStyle}>
                This heatmap shows which numeric columns move together. Darker squares mean stronger relationships, while lighter squares mean weaker or no clear relationship.
              </p>
            ) : stats?.correlation_explanation && (
              typeof stats.correlation_explanation === 'string' ? (
                <p style={explanationStyle}>{stats.correlation_explanation}</p>
              ) : (
                <>
                  {stats.correlation_explanation.layman_summary && (
                    <p style={explanationStyle}>{stats.correlation_explanation.layman_summary}</p>
                  )}
                  {stats.correlation_explanation.narrative && (
                    <p style={{ ...explanationStyle, fontStyle: 'normal', color: '#666', fontSize: '0.85rem' }}>
                      {stats.correlation_explanation.narrative}
                    </p>
                  )}
                </>
              )
            )}
            {/* Pairwise Explanations */}
            {stats?.pair_explanations && stats.pair_explanations.length > 0 && (
              <div style={{ marginTop: '1rem' }}>
                <p style={{ fontWeight: '600', color: '#1B6B5A', marginBottom: '0.5rem' }}>
                  Detailed Pairwise Relationships:
                </p>
                {stats.pair_explanations.map((pair, idx) => (
                  <div key={idx} style={{ marginBottom: '0.75rem', fontSize: '0.85rem' }}>
                    <strong>{pair.x} ↔ {pair.y}</strong> (r = {pair.pearson_r.toFixed(3)})
                    {pair.layman_narrative && (
                      <p style={{ margin: '0.25rem 0', color: '#333' }}>
                        {pair.layman_narrative}
                      </p>
                    )}
                    {pair.narrative && (
                      <p style={{ margin: '0.25rem 0', color: '#666', fontSize: '0.82rem' }}>
                        {pair.narrative}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Pairplot (scatter matrix) */}
      {!isBaseline && charts.pairplot && (
        <div>
          <h3 style={sectionTitleStyle}>Pairwise Scatterplots</h3>
          <div style={chartCardStyle}>
            <img src={`data:image/png;base64,${charts.pairplot}`} alt="Pairwise scatterplots" style={{ width: '100%', height: 'auto', borderRadius: '8px' }} />
            {stats?.pair_explanations?.length > 0 ? (
              <p style={explanationStyle}>
                The pairplot shows how the strongest numeric variables move together. The most notable pair is{' '}
                <strong>{stats.pair_explanations[0].x}</strong> and <strong>{stats.pair_explanations[0].y}</strong>, where the relationship is {stats.pair_explanations[0].strength}.
              </p>
            ) : (
              <p style={explanationStyle}>
                The pairplot compares every numeric column against every other numeric column to reveal clusters, slopes, and outliers.
              </p>
            )}
          </div>
        </div>
      )}

      {/* Violin plots */}
      {!isBaseline && charts.violinplots && charts.violinplots.length > 0 && (
        <div>
          <h3 style={sectionTitleStyle}>Violin Plots</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1rem' }}>
            {charts.violinplots.map((v, i) => (
              <div key={i} style={chartCardStyle}>
                <p style={{ fontWeight: 600, color: '#1B6B5A', marginBottom: 8 }}>{v.column}</p>
                <img src={`data:image/png;base64,${v.image}`} alt={`Violin ${v.column}`} style={{ width: '100%', height: 'auto', borderRadius: '6px' }} />
                {isBaseline ? (
                  <p style={explanationStyle}>
                    This violin plot shows where the values for {v.column} are concentrated and how spread out they are. A wider shape means more variability; a thinner center means more values bunch together.
                  </p>
                ) : stats?.distribution_explanations?.[v.column]?.layman_narrative ? (
                  <p style={explanationStyle}>{stats.distribution_explanations[v.column].layman_narrative}</p>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Missingness Heatmap */}
      {!isBaseline && charts.missingness && (
        <div>
          <h3 style={sectionTitleStyle}>Missing Values</h3>
          <div style={chartCardStyle}>
            <img src={`data:image/png;base64,${charts.missingness}`} alt="Missing values heatmap" style={{ width: '100%', height: 'auto', borderRadius: '8px' }} />
            {isBaseline ? (
              <p style={explanationStyle}>
                This heatmap highlights where data is missing. Blank or highlighted spots mean those values are absent, which is important because missing rows can affect later analysis.
              </p>
            ) : stats?.missing_values ? (
              <p style={explanationStyle}>
                Missingness shows where values are absent. Columns with the largest missing counts should be checked first because they can distort averages, correlations, and outlier counts.
              </p>
            ) : null}
          </div>
        </div>
      )}

      {/* Categorical Bars */}
      {!isBaseline && charts.categorical_bars && charts.categorical_bars.length > 0 && (
        <div>
          <h3 style={sectionTitleStyle}>Categorical Counts</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
            {charts.categorical_bars.map((c, i) => (
              <div key={i} style={chartCardStyle}>
                <p style={{ fontWeight: 600, color: '#1B6B5A', marginBottom: 8 }}>{c.column}</p>
                <img src={`data:image/png;base64,${c.image}`} alt={`Categories ${c.column}`} style={{ width: '100%', height: 'auto', borderRadius: '6px' }} />
                <p style={explanationStyle}>
                  {isBaseline
                    ? 'This bar chart quickly shows which category appears most often. Bigger bars mean that category shows up more in the data.'
                    : 'This bar chart shows category frequency. The tallest bar is the most common category, while smaller bars represent less frequent groups that may need consolidation or special handling.'}
                </p>
              </div>
            ))}
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
                {/* Outlier Explanation (plain-language first) */}
                {isBaseline ? (
                  <p style={explanationStyle}>
                    This box plot gives a quick look at the middle of the data, how spread out it is, and whether there are any unusual values that sit far from the rest.
                  </p>
                ) : stats?.outlier_explanations?.[chart.column]?.layman_narrative ? (
                  <p style={explanationStyle}>
                    {stats.outlier_explanations[chart.column].layman_narrative}
                  </p>
                ) : !isBaseline && stats?.outlier_explanations?.[chart.column]?.narrative ? (
                  <p style={explanationStyle}>
                    {stats.outlier_explanations[chart.column].narrative}
                  </p>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}