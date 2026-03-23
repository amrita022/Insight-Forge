export default function InsightCard({ title, items }) {
  return (
    <div style={{
      background: 'white',
      border: '1px solid #E8E4DC',
      borderLeft: '4px solid #1B6B5A',
      borderRadius: '12px',
      padding: '1.5rem',
      boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
      transition: 'all 0.3s ease',
      cursor: 'default',
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.boxShadow = '0 4px 12px rgba(27, 107, 90, 0.1)';
      e.currentTarget.style.transform = 'translateY(-2px)';
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
      e.currentTarget.style.transform = 'translateY(0)';
    }}>
      <h3 style={{
        fontSize: '1.125rem',
        fontWeight: '700',
        color: '#1B6B5A',
        marginBottom: '1rem',
        paddingBottom: '0.75rem',
        borderBottom: '1px solid #E8E4DC',
        fontFamily: '"Playfair Display", serif',
      }}>
        {title}
      </h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {typeof items === 'string' ? (
          <p style={{
            color: '#333',
            lineHeight: '1.6',
            fontSize: '0.95rem',
            fontFamily: '"DM Sans", sans-serif',
          }}>
            {items}
          </p>
        ) : Array.isArray(items) ? (
          <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
            {items.map((item, index) => (
              <li key={index} style={{
                display: 'flex',
                alignItems: 'flex-start',
                gap: '0.75rem',
                color: '#333',
                fontSize: '0.95rem',
                fontFamily: '"DM Sans", sans-serif',
                marginBottom: '0.5rem',
              }}>
                <span style={{ color: '#1B6B5A', fontWeight: '600', marginTop: '2px', flexShrink: 0 }}>•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </div>
  );
}
