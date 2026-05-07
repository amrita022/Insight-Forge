import React from 'react';

export default function ChartExplain({ result, file }) {
  // result expected to have: extracted_text, details, model_text, fallback_explanation
  const { extracted_text, details, model_text, fallback_explanation, detected_chart_type, supported_uploads } = result || {};

  const tryParseJson = (text) => {
    try {
      const parsed = JSON.parse(text);
      return parsed;
    } catch (e) {
      return null;
    }
  };

  const parsed = tryParseJson(model_text);

  return (
    <div style={{ background: 'white', padding: '1rem', borderRadius: 8, border: '1px solid #E8E4DC' }}>
      <h3 style={{ marginBottom: 8 }}>Chart Explanation</h3>
      {file && (
        <div style={{ marginBottom: 12 }}>
          <img src={URL.createObjectURL(file)} alt="uploaded" style={{ maxWidth: '100%', height: 'auto', borderRadius: 6 }} />
        </div>
      )}

      {/* Prefer a direct fallback explanation when available */}
      {fallback_explanation ? (
        <div style={{ marginBottom: 12 }}>
          <strong>Detected Chart Type:</strong>
          <p style={{ background: '#EEF4FF', padding: 8, borderRadius: 6, textTransform: 'capitalize' }}>
            {(detected_chart_type || fallback_explanation.chart_type || 'unknown_chart').replaceAll('_', ' ')}
          </p>

          <strong>Quick Summary:</strong>
          <p style={{ background: '#F1F8F3', padding: 8, borderRadius: 6 }}>{fallback_explanation.summary}</p>

          <strong>Axis Explanation:</strong>
          <ul style={{ background: '#FFF', padding: 8, borderRadius: 6 }}>
            <li><strong>X:</strong> {fallback_explanation.axis_explanation?.x}</li>
            <li><strong>Y:</strong> {fallback_explanation.axis_explanation?.y}</li>
          </ul>

          <strong>Series Notes:</strong>
          <div style={{ background: '#FFF', padding: 8, borderRadius: 6 }}>
            {fallback_explanation.series_summary.map((s, i) => (
              <div key={i} style={{ marginBottom: 6 }}>
                <strong>{s.name}</strong>: {s.note}
              </div>
            ))}
          </div>

          {fallback_explanation.insights?.length > 0 && (
            <>
              <strong>Key Insights:</strong>
              <ul style={{ background: '#FFF', padding: 8, borderRadius: 6 }}>
                {fallback_explanation.insights.map((insight, i) => (
                  <li key={i}>{insight}</li>
                ))}
              </ul>
            </>
          )}

          <strong>Recommendations:</strong>
          <ul style={{ background: '#FFF', padding: 8, borderRadius: 6 }}>
            {fallback_explanation.recommendations.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>

          {supported_uploads?.chart_types?.length > 0 && (
            <>
              <strong>Supported Chart Categories:</strong>
              <div style={{ background: '#FFF', padding: 8, borderRadius: 6, display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                {supported_uploads.chart_types.map((c, i) => (
                  <span key={i} style={{ background: '#F7F7F7', padding: '4px 8px', borderRadius: 999, fontSize: 12 }}>
                    {c.replaceAll('_', ' ')}
                  </span>
                ))}
              </div>
            </>
          )}
        </div>
      ) : (
        <div>
          <div style={{ marginBottom: 12 }}>
            <strong>Extracted Text (OCR):</strong>
            <pre style={{ whiteSpace: 'pre-wrap', background: '#F7F7F7', padding: 8, borderRadius: 6 }}>{extracted_text || 'No text detected'}</pre>
          </div>

          <div style={{ marginBottom: 12 }}>
            <strong>Heuristic Details:</strong>
            <pre style={{ whiteSpace: 'pre-wrap', background: '#F7F7F7', padding: 8, borderRadius: 6 }}>{JSON.stringify(details || {}, null, 2)}</pre>
          </div>

          <div>
            <strong>Model Explanation:</strong>
            {parsed ? (
              <pre style={{ whiteSpace: 'pre-wrap', background: '#F1F8F3', padding: 8, borderRadius: 6 }}>{JSON.stringify(parsed, null, 2)}</pre>
            ) : (
              <pre style={{ whiteSpace: 'pre-wrap', background: '#F1F8F3', padding: 8, borderRadius: 6 }}>{model_text || 'No explanation returned'}</pre>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
