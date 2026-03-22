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
          className="hidden"
        />
        
        <div className="upload-content">
          <div className="upload-icon">☁️</div>
          <div>
            <p className="upload-text">Drop your CSV file here</p>
            <p className="upload-text-secondary">or click to browse</p>
          </div>
        </div>
      </div>

      {file && (
        <div className="file-selected">
          <span>✓</span>
          <span className="filename-text">{file.name}</span>
        </div>
      )}

      <div className="button-group">
        <button
          onClick={() => onAnalyze(file)}
          disabled={!file || isLoading}
          className="btn btn-primary flex-1 min-w-[200px]"
        >
          {isLoading ? 'Analyzing...' : 'Analyze with AI'}
        </button>
        <button
          onClick={() => onBaseline(file)}
          disabled={!file || isLoading}
          className="btn btn-secondary flex-1 min-w-[200px]"
        >
          {isLoading ? 'Analyzing...' : 'Baseline Analysis'}
        </button>
      </div>
    </div>
  );
}
