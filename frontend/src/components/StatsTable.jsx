export default function StatsTable({ stats }) {
  if (!stats) {
    return null;
  }

  const sectionTitleStyle = {
    fontSize: '1.25rem',
    fontWeight: '700',
    color: '#1B6B5A',
    marginBottom: '1rem',
    fontFamily: '"Playfair Display", serif',
  };

  const statCardStyle = (bgColor) => ({
    background: 'white',
    borderRadius: '12px',
    padding: '1.5rem',
    border: '1px solid #E8E4DC',
    borderTop: `4px solid ${bgColor}`,
    transition: 'all 0.3s ease',
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Shape - 3 Card Grid */}
      {stats.shape && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1rem',
        }}>
          <div style={statCardStyle('#4A90E2')}>
            <p style={{
              color: '#4A90E2',
              fontSize: '0.75rem',
              fontWeight: '700',
              letterSpacing: '0.05em',
              textTransform: 'uppercase',
              marginBottom: '0.5rem',
            }}>
              Rows
            </p>
            <p style={{
              fontSize: '2rem',
              fontWeight: '700',
              color: '#1B6B5A',
              marginTop: '0.5rem',
            }}>
              {stats.shape.rows.toLocaleString()}
            </p>
          </div>
          <div style={statCardStyle('#7B68EE')}>
            <p style={{
              color: '#7B68EE',
              fontSize: '0.75rem',
              fontWeight: '700',
              letterSpacing: '0.05em',
              textTransform: 'uppercase',
              marginBottom: '0.5rem',
            }}>
              Columns
            </p>
            <p style={{
              fontSize: '2rem',
              fontWeight: '700',
              color: '#1B6B5A',
              marginTop: '0.5rem',
            }}>
              {stats.shape.columns}
            </p>
          </div>
          <div style={statCardStyle('#10B981')}>
            <p style={{
              color: '#10B981',
              fontSize: '0.75rem',
              fontWeight: '700',
              letterSpacing: '0.05em',
              textTransform: 'uppercase',
              marginBottom: '0.5rem',
            }}>
              Size
            </p>
            <p style={{
              fontSize: '2rem',
              fontWeight: '700',
              color: '#1B6B5A',
              marginTop: '0.5rem',
            }}>
              {(stats.shape.rows * stats.shape.columns).toLocaleString()}
            </p>
          </div>
        </div>
      )}

      {/* Data Types */}
      {stats.dtypes && (
        <div>
          <h3 style={sectionTitleStyle}>Column Data Types</h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
            gap: '0.75rem',
          }}>
            {Object.entries(stats.dtypes).map(([col, dtype]) => (
              <div
                key={col}
                style={{
                  background: 'white',
                  border: '1px solid #E8E4DC',
                  borderRadius: '12px',
                  padding: '1rem',
                  transition: 'all 0.3s ease',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.boxShadow = '0 4px 12px rgba(27, 107, 90, 0.1)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.boxShadow = 'none';
                }}
              >
                <p style={{
                  color: '#1B6B5A',
                  fontSize: '0.7rem',
                  fontWeight: '700',
                  letterSpacing: '0.05em',
                  textTransform: 'uppercase',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                }}>
                  {col}
                </p>
                <p style={{
                  color: '#333',
                  fontWeight: '600',
                  fontSize: '0.875rem',
                  marginTop: '0.5rem',
                  fontFamily: '"DM Sans", sans-serif',
                }}>
                  {dtype}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Missing Values */}
      {stats.missing_values && Object.values(stats.missing_values).some(v => v > 0) && (
        <div>
          <h3 style={sectionTitleStyle}>Missing Values</h3>
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
            gap: '0.75rem',
          }}>
            {Object.entries(stats.missing_values)
              .filter(([, count]) => count > 0)
              .map(([col, count]) => (
                <div
                  key={col}
                  style={statCardStyle('#EF4444')}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.boxShadow = '0 4px 12px rgba(239, 68, 68, 0.1)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                >
                  <p style={{
                    color: '#1B6B5A',
                    fontSize: '0.7rem',
                    fontWeight: '700',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}>
                    {col}
                  </p>
                  <p style={{
                    color: '#EF4444',
                    fontWeight: '700',
                    fontSize: '1.5rem',
                    marginTop: '0.5rem',
                  }}>
                    {count}
                  </p>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Descriptive Statistics */}
      {stats.descriptive_stats && Object.keys(stats.descriptive_stats).length > 0 && (
        <div>
          <h3 style={sectionTitleStyle}>Summary Statistics</h3>
          <div style={{ overflowX: 'auto' }}>
            <table style={{
              width: '100%',
              borderCollapse: 'collapse',
              fontFamily: '"DM Sans", sans-serif',
            }}>
              <thead>
                <tr style={{
                  background: '#FAF8F3',
                  borderBottom: '2px solid #1B6B5A',
                }}>
                  <th style={{
                    padding: '1rem',
                    textAlign: 'left',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    color: '#1B6B5A',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                  }}>
                    Column
                  </th>
                  <th style={{
                    padding: '1rem',
                    textAlign: 'left',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    color: '#1B6B5A',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                  }}>
                    Count
                  </th>
                  <th style={{
                    padding: '1rem',
                    textAlign: 'left',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    color: '#1B6B5A',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                  }}>
                    Mean
                  </th>
                  <th style={{
                    padding: '1rem',
                    textAlign: 'left',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    color: '#1B6B5A',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                  }}>
                    Median
                  </th>
                  <th style={{
                    padding: '1rem',
                    textAlign: 'left',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    color: '#1B6B5A',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                  }}>
                    Std Dev
                  </th>
                  <th style={{
                    padding: '1rem',
                    textAlign: 'left',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    color: '#1B6B5A',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                  }}>
                    Min
                  </th>
                  <th style={{
                    padding: '1rem',
                    textAlign: 'left',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    color: '#1B6B5A',
                    letterSpacing: '0.05em',
                    textTransform: 'uppercase',
                  }}>
                    Max
                  </th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(stats.descriptive_stats).map(([col, stat], idx) => (
                  <tr
                    key={col}
                    style={{
                      background: idx % 2 === 0 ? 'white' : '#FAF8F3',
                      borderBottom: '1px solid #E8E4DC',
                      transition: 'background-color 0.2s ease',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = '#F5FBF9';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = idx % 2 === 0 ? 'white' : '#FAF8F3';
                    }}
                  >
                    <td style={{
                      padding: '0.875rem 1rem',
                      fontSize: '0.875rem',
                      fontWeight: '500',
                      color: '#1B6B5A',
                    }}>
                      {col}
                    </td>
                    <td style={{
                      padding: '0.875rem 1rem',
                      fontSize: '0.875rem',
                      color: '#333',
                    }}>
                      {stat.count}
                    </td>
                    <td style={{
                      padding: '0.875rem 1rem',
                      fontSize: '0.875rem',
                      color: '#333',
                    }}>
                      {stat.mean !== null ? stat.mean.toFixed(2) : 'N/A'}
                    </td>
                    <td style={{
                      padding: '0.875rem 1rem',
                      fontSize: '0.875rem',
                      color: '#333',
                    }}>
                      {stat.median !== null ? stat.median.toFixed(2) : 'N/A'}
                    </td>
                    <td style={{
                      padding: '0.875rem 1rem',
                      fontSize: '0.875rem',
                      color: '#333',
                    }}>
                      {stat.std !== null ? stat.std.toFixed(2) : 'N/A'}
                    </td>
                    <td style={{
                      padding: '0.875rem 1rem',
                      fontSize: '0.875rem',
                      color: '#333',
                    }}>
                      {stat.min !== null ? stat.min.toFixed(2) : 'N/A'}
                    </td>
                    <td style={{
                      padding: '0.875rem 1rem',
                      fontSize: '0.875rem',
                      color: '#333',
                    }}>
                      {stat.max !== null ? stat.max.toFixed(2) : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
