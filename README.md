# Insight Forge

<div align="center">

![Insight Forge Logo](https://img.shields.io/badge/Insight%20Forge-Data%20Analysis-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJDMTMuMSAyIDE0IDIuOSAxNCA0VjE2QzE0IDE3LjEgMTMuMSAxOCA5LjUgMTguNUM3LjkgMTguNSA3IDE3LjYgNyAxNlY0QzcgMi45IDcuOSAyIDkgMkgxNUMxNS4xIDIgMTYgMi45IDE2IDRWMTZDMTYgMTcuMSAxNS4xIDE4IDEzLjUgMTguNUMxMS45IDE4LjUgMTEgMTcuNiAxMSAxNlY0QzExIDIuOSAxMS45IDIgMTMgMkgxNloiIGZpbGw9IiMzQjgxRjYiLz4KPC9zdmc+)

**Revolutionizing Data Analysis with AI-Powered Insights**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-🚀-brightgreen?style=flat-square)](https://insight-forge-eta.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python)](https://python.org)
[![React](https://img.shields.io/badge/React-19-61dafb.svg?style=flat-square&logo=react)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI-orange.svg?style=flat-square&logo=google)](https://ai.google.dev/)

*Upload CSV files, get instant EDA with AI insights powered by Google's Gemini*

[Features](#-features) • [Quick Start](#-quick-start) • [Tech Stack](#️-tech-stack) • [Usage](#-usage-guide)

</div>

---

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [🌐 Live Demo](#-live-demo)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📋 Prerequisites](#-prerequisites)
- [🚀 Quick Start](#-quick-start)
- [🐳 Docker Deployment](#-docker-deployment)
- [📖 Usage Guide](#-usage-guide)
- [📁 Project Structure](#-project-structure)

---

## 🌟 Overview

Insight Forge is a cutting-edge full-stack web application that transforms the way you perform exploratory data analysis (EDA). By combining automated statistical analysis with Google's Gemini AI, it provides instant, comprehensive insights from your CSV datasets.

### 🎯 What Makes It Special

- **🤖 AI-Powered Analysis**: Leverages Google's Gemini AI for intelligent data insights
- **⚡ One-Click EDA**: Complete analysis pipeline with a single file upload
- **📊 Rich Visualizations**: Interactive charts and statistical summaries
- **🔄 Dual Analysis Modes**: Choose between comprehensive or focused analysis
- **🎨 Modern Interface**: Beautiful, responsive web application
- **⚙️ Developer-Friendly**: RESTful API with comprehensive documentation

---

## 🌐 Live Demo

🚀 **[Try Insight Forge Live](https://insight-forge-eta.vercel.app/)**

Experience the full power of Insight Forge without any setup!

---

## ✨ Features

### 🔬 Core Analysis Capabilities

- **🚀 Automated EDA Pipeline**
  - Data type detection and validation
  - Missing value analysis
  - Statistical summaries (mean, median, std, quartiles)
  - Correlation analysis for numeric data
  - Outlier detection

- **📊 Advanced Statistics**
  - Descriptive statistics for all numeric columns
  - Data distribution analysis
  - Correlation matrices
  - Outlier identification and counting

- **📈 Interactive Visualizations**
  - Matplotlib and Seaborn-powered charts
  - Multiple chart types (histograms, scatter plots, box plots)
  - High-quality PNG exports

### 🤖 AI-Powered Insights

- **🧠 Gemini AI Integration**
  - Context-aware data analysis
  - Natural language insights and recommendations
  - Pattern recognition and anomaly detection
  - Actionable business intelligence

- **🔄 Analysis Modes**
  - **Full Analysis**: Complete EDA + AI insights + visualizations
  - **Baseline Analysis**: Quick AI analysis on raw data samples

### 🎨 User Experience

- **📱 Responsive Design**
  - Mobile-first approach
  - Clean, modern interface
  - Intuitive drag-and-drop file upload

- **⚡ Performance Optimized**
  - FastAPI backend for high throughput
  - Efficient data processing with pandas
  - Optimized AI prompt engineering

### 🛠️ Developer Features

- **🔌 RESTful API**
  - Well-documented endpoints
  - JSON responses
  - CORS enabled for web integration

- **🐳 Containerization**
  - Docker support for easy deployment
  - Environment-based configuration
  - Production-ready setup

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **FastAPI** - High-performance web framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Matplotlib & Seaborn** - Data visualization
- **Google Gemini AI** - AI insights generation
- **python-multipart** - File upload handling
- **Uvicorn** - ASGI server

### Frontend
- **React 19** - UI library with hooks and concurrent features
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Lucide React** - Icon library
- **Axios** - HTTP client (if used)

### DevOps & Deployment
- **Docker** - Containerization
- **Vercel** - Frontend deployment
- **Environment Variables** - Configuration management

### Development Tools
- **ESLint** - JavaScript linting
- **Prettier** - Code formatting
- **Python venv** - Virtual environment management

---

## 📋 Prerequisites

Before running Insight Forge, ensure you have:

### System Requirements
- **Python 3.8 or higher**
- **Node.js 16 or higher**
- **Docker** (optional, for containerized deployment)

### API Keys
- **Google Gemini API Key** - Required for AI insights
  - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
  - Free tier available with generous limits

### Optional
- **Git** - For cloning the repository
- **VS Code** - Recommended IDE with Python and React extensions

---

## 🚀 Quick Start

Get Insight Forge running in under 5 minutes!

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/insight-forge.git
cd insight-forge
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🐳 Docker Deployment

### Backend Only

```bash
cd backend

# Build Docker image
docker build -t insight-forge-backend .

# Run container
docker run -p 8000:8000 -e GEMINI_API_KEY=your_api_key_here insight-forge-backend
```

### Full Stack Deployment

```bash
# Backend container
docker run -d --name insight-forge-backend \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  --restart unless-stopped \
  insight-forge-backend

# Frontend (build and serve)
cd frontend
npm run build
npm run preview  # or deploy dist/ folder
```

---

## 📖 Usage Guide

### Basic Workflow

1. **Access the Application**
   - Open http://localhost:5173 in your browser

2. **Upload Data**
   - Drag and drop a CSV file or click to browse
   - Supported format: CSV files only
   - Maximum file size: Depends on your configuration

3. **Choose Analysis Mode**
   - **Full Analysis**: Complete EDA with stats, charts, and AI insights
   - **Baseline Analysis**: Quick AI analysis on raw data samples

4. **Review Results**
   - **Statistics**: Data overview, missing values, distributions
   - **Charts**: Visual representations of your data
   - **AI Insights**: Intelligent analysis and recommendations

### Supported Data Formats

- **File Type**: CSV (comma-separated values)
- **Encoding**: UTF-8 recommended
- **Headers**: First row should contain column names
- **Data Types**: Automatic detection (numeric, categorical, text)

### Analysis Output

#### Statistics Section
- Dataset shape (rows × columns)
- Column data types
- Missing value counts
- Descriptive statistics (mean, median, std, quartiles)
- Correlation matrix (for numeric columns)

#### Charts Section
- Histograms for numeric distributions
- Box plots for outlier detection
- Scatter plots for correlations
- Bar charts for categorical data

#### AI Insights Section
- Natural language analysis summary
- Key findings and patterns
- Recommendations for further analysis
- Potential issues or anomalies

---

## 📁 Project Structure

```
insight-forge/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app, routes, CORS
│   │   ├── eda_engine.py        # Core EDA analysis functions
│   │   ├── gemini_client.py     # Gemini AI API integration
│   │   ├── prompt_builder.py    # AI prompt construction utilities
│   │   ├── charts.py            # Chart generation with matplotlib/seaborn
│   │   └── __pycache__/         # Python bytecode cache
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile               # Backend container configuration
│   └── .env.example             # Environment variables template
├── frontend/
│   ├── public/
│   │   └── vite.svg             # Vite logo
│   ├── src/
│   │   ├── App.jsx              # Main React app component
│   │   ├── main.jsx             # React app entry point
│   │   ├── index.css            # Global styles
│   │   ├── LandingPage.jsx      # Landing page component
│   │   └── components/
│   │       ├── UploadZone.jsx   # File upload interface
│   │       ├── InsightCard.jsx  # AI insights display
│   │       ├── ChartPanel.jsx   # Chart visualization
│   │       └── StatsTable.jsx   # Statistics table
│   ├── index.html               # HTML template
│   ├── package.json             # Node.js dependencies and scripts
│   ├── vite.config.js           # Vite build configuration
│   ├── tailwind.config.js       # Tailwind CSS configuration
│   ├── eslint.config.js         # ESLint configuration
│   └── README.md                # Frontend-specific documentation
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

### Key Files Explanation

- **`backend/app/main.py`**: Core FastAPI application with API endpoints
- **`backend/app/eda_engine.py`**: Pandas-based data analysis functions
- **`backend/app/gemini_client.py`**: Google Gemini AI integration
- **`frontend/src/App.jsx`**: Main React application with routing
- **`frontend/src/components/`**: Reusable UI components

---

<div align="center">

**Built with ❤️ using React, FastAPI, and Google's Gemini AI**

⭐ **Star this repo** if you find it useful!

[⬆️ Back to Top](#insight-forge)

</div>