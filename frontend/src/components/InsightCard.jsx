import '../styles/InsightCard.css';

export default function InsightCard({ title, items }) {
  return (
    <div className="insight-card">
      <h3 className="card-title">{title}</h3>
      <div className="card-content">
        {typeof items === 'string' ? (
          <p className="card-text">{items}</p>
        ) : Array.isArray(items) ? (
          <ul className="card-list">
            {items.map((item, index) => (
              <li key={index} className="list-item">
                {item}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </div>
  );
}
