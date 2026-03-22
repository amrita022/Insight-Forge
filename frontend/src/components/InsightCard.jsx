export default function InsightCard({ title, items }) {
  return (
    <div className="insight-card">
      <h3 className="insight-title">{title}</h3>
      <div className="card-content">
        {typeof items === 'string' ? (
          <p className="card-text">{items}</p>
        ) : Array.isArray(items) ? (
          <ul className="insight-list">
            {items.map((item, index) => (
              <li key={index} className="insight-item">
                {item}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </div>
  );
}
