import '../styles/StatsTable.css';

export default function StatsTable({ stats }) {
  if (!stats) {
    return null;
  }

  return (
    <div className="stats-table-container">
      {/* Shape */}
      {stats.shape && (
        <div className="stats-section">
          <h3 className="stats-title">Dataset Shape</h3>
          <table className="stats-table">
            <tbody>
              <tr>
                <td className="label">Rows</td>
                <td className="value">{stats.shape.rows.toLocaleString()}</td>
              </tr>
              <tr>
                <td className="label">Columns</td>
                <td className="value">{stats.shape.columns}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* Data Types */}
      {stats.dtypes && (
        <div className="stats-section">
          <h3 className="stats-title">Column Data Types</h3>
          <table className="stats-table">
            <thead>
              <tr>
                <th>Column</th>
                <th>Data Type</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(stats.dtypes).map(([col, dtype]) => (
                <tr key={col}>
                  <td className="label">{col}</td>
                  <td className="value">{dtype}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Missing Values */}
      {stats.missing_values && Object.values(stats.missing_values).some(v => v > 0) && (
        <div className="stats-section">
          <h3 className="stats-title">Missing Values</h3>
          <table className="stats-table">
            <thead>
              <tr>
                <th>Column</th>
                <th>Missing Count</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(stats.missing_values)
                .filter(([, count]) => count > 0)
                .map(([col, count]) => (
                  <tr key={col}>
                    <td className="label">{col}</td>
                    <td className="value">{count}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
