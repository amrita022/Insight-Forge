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

      {/* Descriptive Statistics */}
      {stats.descriptive_stats && Object.keys(stats.descriptive_stats).length > 0 && (
        <div className="stats-section">
          <h3 className="stats-section-title">Summary Statistics</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-300 rounded-lg">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Column</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Count</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Mean</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Median</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Std Dev</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Min</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Max</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {Object.entries(stats.descriptive_stats).map(([col, stat]) => (
                  <tr key={col}>
                    <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">{col}</td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{stat.count}</td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                      {stat.mean !== null ? stat.mean.toFixed(2) : 'N/A'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                      {stat.median !== null ? stat.median.toFixed(2) : 'N/A'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                      {stat.std !== null ? stat.std.toFixed(2) : 'N/A'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                      {stat.min !== null ? stat.min.toFixed(2) : 'N/A'}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
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
