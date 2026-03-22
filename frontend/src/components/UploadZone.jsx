import { useState, useRef } from 'react';
import '../styles/UploadZone.css';

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
    <div className="upload-zone-container">
      <div
        className={`upload-zone ${isDragActive ? 'active' : ''}`}
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
          className="file-input"
        />
        
        <div className="upload-content">
          <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p className="upload-text">
            Drag and drop your CSV file here
            <br />
            or click to browse
          </p>
        </div>
      </div>

      {file && (
        <div className="file-selected">
          <svg className="check-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z" />
          </svg>
          <span className="filename">{file.name}</span>
        </div>
      )}

      <div className="button-group">
        <button
          onClick={() => onAnalyze(file)}
          disabled={!file || isLoading}
          className="btn btn-primary"
        >
          {isLoading ? 'Analyzing...' : 'Analyze with Insight Forge'}
        </button>
        <button
          onClick={() => onBaseline(file)}
          disabled={!file || isLoading}
          className="btn btn-secondary"
        >
          {isLoading ? 'Analyzing...' : 'Baseline Analysis'}
        </button>
      </div>
    </div>
  );
}
