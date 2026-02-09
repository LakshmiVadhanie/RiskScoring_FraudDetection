from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Request
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from database.models import Transaction, Alert
from database.connection import get_db
from ml_models.ensemble_scorer import EnsembleScorer
from features.transaction_features import TransactionFeatureEngine

router = APIRouter()
scorer = EnsembleScorer()
feature_engine = TransactionFeatureEngine()

class TransactionRequest(BaseModel):
    user_id: str
    merchant_id: str
    amount: float = Field(..., gt=0)
    currency: str = "USD"
    country: str
    device_id: str
    ip_address: str
    transaction_type: str
    channel: str

class TransactionResponse(BaseModel):
    transaction_id: str
    risk_score: float
    risk_level: str
    is_fraud: bool
    fraud_probability: float
    decision: str
    reasons: List[str]
    model_scores: Dict[str, float]
    timestamp: datetime

def get_risk_level(score: float) -> str:
    if score >= 0.8: return "CRITICAL"
    elif score >= 0.6: return "HIGH"
    elif score >= 0.4: return "MEDIUM"
    elif score >= 0.2: return "LOW"
    return "MINIMAL"

def get_decision(score: float) -> str:
    if score >= 0.8: return "BLOCK"
    elif score >= 0.6: return "REVIEW"
    return "APPROVE"

async def broadcast_alert(ws_manager, data: dict):
    if hasattr(ws_manager, 'broadcast'):
        await ws_manager.broadcast({"type": "fraud_alert", "data": data})

@router.post("/score", response_model=TransactionResponse)
async def score_transaction(
    req: TransactionRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    transaction_id = str(uuid.uuid4())
    
    # Extract features
    features = feature_engine.extract_features(req.dict())
    
    # Get predictions
    result = scorer.predict(features)
    
    risk_score = result['ensemble_score']
    risk_level = get_risk_level(risk_score)
    decision = get_decision(risk_score)
    is_fraud = risk_score >= 0.6
    
    # Save to database
    db_transaction = Transaction(
        id=transaction_id,
        user_id=req.user_id,
        merchant_id=req.merchant_id,
        amount=req.amount,
        currency=req.currency,
        country=req.country,
        device_id=req.device_id,
        ip_address=req.ip_address,
        transaction_type=req.transaction_type,
        channel=req.channel,
        risk_score=risk_score,
        risk_level=risk_level,
        is_fraud=is_fraud,
        fraud_probability=result['fraud_probability'],
        decision=decision,
        model_scores=result['model_scores'],
        reasons=result['reasons']
    )
    
    db.add(db_transaction)
    await db.commit()
    
    # Create alert if high risk
    if risk_score >= 0.6:
        alert = Alert(
            transaction_id=transaction_id,
            alert_type="HIGH_RISK_TRANSACTION",
            severity=risk_level,
            message=f"High risk transaction detected: ${req.amount}",
            details=result
        )
        db.add(alert)
        await db.commit()
        
        # Broadcast via WebSocket
        alert_data = {
            "transaction_id": transaction_id,
            "user_id": req.user_id,
            "amount": req.amount,
            "risk_score": risk_score,
            "risk_level": risk_level
        }
        background_tasks.add_task(broadcast_alert, request.app.state.ws_manager, alert_data)
    
    return TransactionResponse(
        transaction_id=transaction_id,
        risk_score=risk_score,
        risk_level=risk_level,
        is_fraud=is_fraud,
        fraud_probability=result['fraud_probability'],
        decision=decision,
        reasons=result['reasons'],
        model_scores=result['model_scores'],
        timestamp=datetime.utcnow()
    )

@router.get("/recent")
async def get_recent_transactions(
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transaction)
        .order_by(Transaction.created_at.desc())
        .limit(limit)
    )
    transactions = result.scalars().all()
    
    return [{
        "id": t.id,
        "user_id": t.user_id,
        "amount": t.amount,
        "risk_score": t.risk_score,
        "risk_level": t.risk_level,
        "decision": t.decision,
        "created_at": t.created_at.isoformat()
    } for t in transactions]

@router.get("/{transaction_id}")
async def get_transaction(
    transaction_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Transaction).where(Transaction.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return {
        "id": transaction.id,
        "user_id": transaction.user_id,
        "merchant_id": transaction.merchant_id,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "country": transaction.country,
        "device_id": transaction.device_id,
        "risk_score": transaction.risk_score,
        "risk_level": transaction.risk_level,
        "is_fraud": transaction.is_fraud,
        "fraud_probability": transaction.fraud_probability,
        "decision": transaction.decision,
        "reasons": transaction.reasons,
        "model_scores": transaction.model_scores,
        "created_at": transaction.created_at.isoformat()
    }