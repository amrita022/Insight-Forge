import { useState, useRef } from 'react';

export default function UploadZone({ onAnalyze, onBaseline, onImageExplain, file, isLoading, onFileSelect }) {
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef(null);
  const imageInputRef = useRef(null);

  const buttonStyle = {
    flex: 1,
    padding: '0.875rem 1.5rem',
    background: '#1B6B5A',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '1rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    opacity: isLoading ? 0.6 : 1,
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragActive(true);
    } else if (e.type === 'dragleave') {
      setIsDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles && droppedFiles[0]) {
      const droppedFile = droppedFiles[0];
      const dataTransfer = new DataTransfer();
      dataTransfer.items.add(droppedFile);

      if (droppedFile.name.endsWith('.csv')) {
        if (fileInputRef.current) {
          fileInputRef.current.files = dataTransfer.files;
          fileInputRef.current.dispatchEvent(new Event('change', { bubbles: true }));
        }
      } else if (/\.(png|jpg|jpeg|bmp|gif)$/i.test(droppedFile.name)) {
        if (imageInputRef.current) {
          imageInputRef.current.files = dataTransfer.files;
          imageInputRef.current.dispatchEvent(new Event('change', { bubbles: true }));
        }
      }
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (onFileSelect) {
        onFileSelect(selectedFile);
      }
    }
  };

  const handleCsvClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      <div
        style={{
          border: `2px dashed ${isDragActive ? '#1B6B5A' : '#1B6B5A'}`,
          backgroundColor: isDragActive ? '#F5FBF9' : '#FAF8F3',
          borderRadius: '12px',
          padding: '3rem',
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          minHeight: '200px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleCsvClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleChange}
          style={{ display: 'none' }}
        />
        <input
          ref={imageInputRef}
          type="file"
          accept=".png,.jpg,.jpeg,.bmp,.gif"
          onChange={handleChange}
          style={{ display: 'none' }}
        />

        <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>📁</div>
        <p style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1B6B5A', marginBottom: '0.5rem' }}>
          Drop your CSV or chart image here
        </p>
        <p style={{ fontSize: '0.95rem', color: '#666' }}>or click to browse CSV files</p>
      </div>

      {file && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            background: '#E3F2FD',
            color: '#1B6B5A',
            padding: '0.75rem 1rem',
            borderRadius: '24px',
            fontSize: '0.95rem',
            fontWeight: '600',
          }}
        >
          <span>✓</span>
          <span>{file.name}</span>
        </div>
      )}

      <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
        <button onClick={onAnalyze} disabled={isLoading} style={buttonStyle}>
          Analyze (Full)
        </button>
        <button
          onClick={onBaseline}
          disabled={isLoading}
          style={{ ...buttonStyle, backgroundColor: '#fff', color: '#1B6B5A', border: '1px solid #1B6B5A' }}
        >
          Quick Baseline
        </button>
        <button
          onClick={() => imageInputRef.current?.click()}
          disabled={isLoading}
          style={{ ...buttonStyle, backgroundColor: '#F7FAF8', color: '#1B6B5A', border: '1px dashed #1B6B5A' }}
        >
          Select Chart Image
        </button>
        <button
          onClick={onImageExplain}
          disabled={isLoading}
          style={{ ...buttonStyle, backgroundColor: '#E6F6EE', color: '#1B6B5A' }}
        >
          Explain Chart Image
        </button>
      </div>
    </div>
  );
}
