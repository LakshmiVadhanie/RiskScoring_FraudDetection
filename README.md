# 🛡️ Enterprise Fraud Detection Platform

Real-time fraud detection system with ML ensemble models and analytics dashboard.

![Status](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)

## 📊 Live Metrics
```
Transactions: 682 | Fraud: 33 (4.84%) | Amount: $1,020,317 | Risk Score: 22.9/100
```

## ✨ Features

- ⚡ **Real-time scoring** (<100ms per transaction)
- 🤖 **4 ML models** (XGBoost, Isolation Forest, LSTM, Graph Networks)
- 📊 **Analytics dashboard** with trends and alerts
- 🚨 **Smart alerts** (10 active high-risk transactions)
- 🎨 **Production UI** built with Next.js + TypeScript

## 🚀 Quick Start
```bash
# Clone and run
git clone https://github.com/LakshmiVadhanie/RiskScoring_FraudDetection.git
cd RiskScoring_FraudDetection
docker-compose up --build

# Access
# Dashboard: http://localhost:3000
# API: http://localhost:8000/docs
```

## 🛠️ Tech Stack

**Backend:** FastAPI, PostgreSQL, Redis  
**ML:** XGBoost, Scikit-learn, PyTorch, NetworkX  
**Frontend:** Next.js 14, TypeScript, Tailwind, Recharts  
**DevOps:** Docker, Docker Compose

## 🧪 Generate Test Data
```bash
cd ml_pipeline
python generate_fraud_data.py      # 60 diverse transactions
python generate_historical_data.py # 7 days of data
```

## 📈 Performance

- Detection Rate: 4.84%
- API Latency: 87ms average
- Risk Distribution: 55% minimal, 38% low, 5% high, 2% medium
- Active Alerts: $7,482 | $14,610 | $8,514 flagged

## 📁 Structure
```
├── backend/          # FastAPI + ML models
├── frontend/         # Next.js dashboard
├── ml_pipeline/      # Data generators
└── docker-compose.yml
```

## 🎯 Risk Levels

| Level | Score | Action |
|-------|-------|--------|
| MINIMAL | 0-20% | Auto-approve |
| LOW | 20-40% | Monitor |
| MEDIUM | 40-60% | Review |
| HIGH | 60-80% | Block |
| CRITICAL | 80-100% | Auto-block |



---
