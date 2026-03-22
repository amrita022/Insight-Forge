export default function StatsTable({ stats }) {
  if (!stats) {
    return null;
  }

  return (
    <div className="stats-table-container">
      {/* Shape - 3 Card Grid */}
      {stats.shape && (
        <div className="stats-row">
          <div className="stat-card">
            <p className="stat-label">Rows</p>
            <p className="stat-value">{stats.shape.rows.toLocaleString()}</p>
          </div>
          <div className="stat-card">
            <p className="stat-label">Columns</p>
            <p className="stat-value">{stats.shape.columns}</p>
          </div>
          <div className="stat-card">
            <p className="stat-label">Size</p>
            <p className="stat-value">{(stats.shape.rows * stats.shape.columns).toLocaleString()}</p>
          </div>
        </div>
      )}

      {/* Data Types */}
      {stats.dtypes && (
        <div className="stats-section">
          <h3 className="stats-section-title">Column Data Types</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {Object.entries(stats.dtypes).map(([col, dtype]) => (
              <div key={col} className="stat-card">
                <p className="stat-label truncate">{col}</p>
                <p className="stat-value text-sm">{dtype}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Missing Values */}
      {stats.missing_values && Object.values(stats.missing_values).some(v => v > 0) && (
        <div className="stats-section">
          <h3 className="stats-section-title">Missing Values</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {Object.entries(stats.missing_values)
              .filter(([, count]) => count > 0)
              .map(([col, count]) => (
                <div key={col} className="stat-card">
                  <p className="stat-label truncate">{col}</p>
                  <p className="stat-value">{count}</p>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
