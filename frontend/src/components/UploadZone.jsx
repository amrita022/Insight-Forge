import { useState, useRef } from 'react';

export default function UploadZone({ onAnalyze, onBaseline, file, isLoading, onFileSelect }) {
  const [isDragActive, setIsDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setIsDragActive(true);
    } else if (e.type === "dragleave") {
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
      if (droppedFile.name.endsWith('.csv')) {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(droppedFile);
        if (fileInputRef.current) {
          fileInputRef.current.files = dataTransfer.files;
          const changeEvent = new Event('change', { bubbles: true });
          fileInputRef.current.dispatchEvent(changeEvent);
        }
      }
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      if (selectedFile.name.endsWith('.csv') && onFileSelect) {
        onFileSelect(selectedFile);
      }
    }
  };

  const handleClick = () => {
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
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleChange}
          style={{ display: 'none' }}
        />
        
        <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>📁</div>
        <p style={{ fontSize: '1.125rem', fontWeight: '600', color: '#1B6B5A', marginBottom: '0.5rem' }}>Drop your CSV file here</p>
        <p style={{ fontSize: '0.95rem', color: '#666' }}>or click to browse</p>
      </div>

      {file && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          background: '#E3F2FD',
          color: '#1B6B5A',
          padding: '0.75rem 1rem',
          borderRadius: '24px',
          fontSize: '0.95rem',
          fontWeight: '600',
        }}>
          <span>✓</span>
          <span>{file.name}</span>
        </div>
      )}

      <div style={{ display: 'flex', gap: '1rem' }}>
        <button
          onClick={() => onAnalyze(file)}
          disabled={!file || isLoading}
          style={{
            flex: 1,
            padding: '0.875rem 1.5rem',
            background: !file || isLoading ? '#E8E4DC' : '#1B6B5A',
            color: !file || isLoading ? '#999' : 'white',
            border: 'none',
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: !file || isLoading ? 'not-allowed' : 'pointer',
            transition: 'all 0.3s ease',
            opacity: !file || isLoading ? 0.6 : 1,
          }}
          onMouseOver={(e) => {
            if (file && !isLoading) {
              e.target.style.background = '#0f4935';
              e.target.style.transform = 'translateY(-2px)';
            }
          }}
          onMouseOut={(e) => {
            if (file && !isLoading) {
              e.target.style.background = '#1B6B5A';
              e.target.style.transform = 'translateY(0)';
            }
          }}
        >
          {isLoading ? 'Analyzing...' : 'Analyze with AI'}
        </button>
        <button
          onClick={() => onBaseline(file)}
          disabled={!file || isLoading}
          style={{
            flex: 1,
            padding: '0.875rem 1.5rem',
            background: 'white',
            color: !file || isLoading ? '#999' : '#1B6B5A',
            border: `2px solid ${!file || isLoading ? '#E8E4DC' : '#1B6B5A'}`,
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: !file || isLoading ? 'not-allowed' : 'pointer',
            transition: 'all 0.3s ease',
            opacity: !file || isLoading ? 0.6 : 1,
          }}
          onMouseOver={(e) => {
            if (file && !isLoading) {
              e.target.style.background = '#1B6B5A';
              e.target.style.color = 'white';
              e.target.style.transform = 'translateY(-2px)';
            }
          }}
          onMouseOut={(e) => {
            if (file && !isLoading) {
              e.target.style.background = 'white';
              e.target.style.color = '#1B6B5A';
              e.target.style.transform = 'translateY(0)';
            }
          }}
        >
          {isLoading ? 'Analyzing...' : 'Baseline Analysis'}
        </button>
      </div>
    </div>
  );
}
