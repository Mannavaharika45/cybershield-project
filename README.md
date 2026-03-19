# 🛡️ CyberShield — AI-Powered Fake News & Scam Detection

A full-stack cybersecurity web application that detects **fake news**, **phishing links**, **scam messages**, and analyzes **suspicious screenshots** using Machine Learning.

## ✨ Features

- 🗞️ **Fake News Detection** — TF-IDF + Logistic Regression NLP model
- 🔗 **Phishing Link Scanner** — Heuristic URL analysis with 10+ risk signals
- 💬 **Scam Message Analyzer** — Trained on 100+ real scam patterns
- 📷 **Screenshot OCR Patrol** — Tesseract OCR + scam analysis on uploaded images
- 🔐 **User Authentication** — JWT-based signup/login with MongoDB
- 💡 **Cyber Safety Tips** — Educational content for everyday users

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, Tailwind CSS, Vanilla JS |
| Backend | Python FastAPI |
| ML Models | scikit-learn (TF-IDF + Logistic Regression) |
| OCR | Tesseract |
| Database | MongoDB (Motor async driver) |
| Auth | JWT (python-jose) + bcrypt |

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- MongoDB running locally
- Tesseract OCR installed

### 1. Install dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Start the backend
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Start the frontend
```bash
python -m http.server 8082 -d frontend
```

### 4. Open in browser
```
http://localhost:8082
```

## 📁 Project Structure

```
fn/
├── backend/
│   ├── api/            # Route handlers (detection + auth)
│   ├── auth/           # JWT handler
│   ├── models/         # Pydantic schemas
│   ├── services/       # ML models, phishing, OCR, database
│   └── main.py         # FastAPI app entry point
├── frontend/
│   ├── css/style.css   # Custom dark glassmorphism theme
│   ├── js/             # app.js + auth.js
│   └── *.html          # All pages
└── requirements.txt
```
