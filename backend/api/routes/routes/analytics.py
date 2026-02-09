from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Integer
from datetime import datetime, timedelta

from database.models import Transaction, Alert
from database.connection import get_db

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    # Total transactions
    total_result = await db.execute(select(func.count(Transaction.id)))
    total_transactions = total_result.scalar() or 0
    
    # Fraud count
    fraud_result = await db.execute(
        select(func.count(Transaction.id)).where(Transaction.is_fraud == True)
    )
    fraud_count = fraud_result.scalar() or 0
    
    # Risk distribution
    risk_dist_result = await db.execute(
        select(Transaction.risk_level, func.count(Transaction.id))
        .group_by(Transaction.risk_level)
    )
    risk_distribution = {row[0]: row[1] for row in risk_dist_result}
    
    # Decision distribution
    decision_result = await db.execute(
        select(Transaction.decision, func.count(Transaction.id))
        .group_by(Transaction.decision)
    )
    decision_distribution = {row[0]: row[1] for row in decision_result}
    
    # Average risk score
    avg_score_result = await db.execute(select(func.avg(Transaction.risk_score)))
    avg_risk_score = float(avg_score_result.scalar() or 0)
    
    # Total amount processed
    amount_result = await db.execute(select(func.sum(Transaction.amount)))
    total_amount = float(amount_result.scalar() or 0)
    
    # Unresolved alerts
    alert_result = await db.execute(
        select(func.count(Alert.id)).where(Alert.resolved == False)
    )
    unresolved_alerts = alert_result.scalar() or 0
    
    return {
        "total_transactions": total_transactions,
        "fraud_detected": fraud_count,
        "fraud_rate": fraud_count / total_transactions if total_transactions > 0 else 0,
        "average_risk_score": avg_risk_score,
        "total_amount_processed": total_amount,
        "risk_distribution": risk_distribution,
        "decision_distribution": decision_distribution,
        "unresolved_alerts": unresolved_alerts
    }

@router.get("/trends")
async def get_trends(days: int = 7, db: AsyncSession = Depends(get_db)):
    """Get transaction trends - returns data for each day"""
    
    # Get all transactions
    result = await db.execute(
        select(Transaction)
        .order_by(Transaction.created_at)
    )
    transactions = result.scalars().all()
    
    if not transactions:
        # Return empty trend data if no transactions
        return []
    
    # Group by date
    from collections import defaultdict
    daily_data = defaultdict(lambda: {'total': 0, 'fraud': 0, 'risk_sum': 0.0})
    
    for txn in transactions:
        date_key = txn.created_at.date().isoformat()
        daily_data[date_key]['total'] += 1
        if txn.is_fraud:
            daily_data[date_key]['fraud'] += 1
        daily_data[date_key]['risk_sum'] += txn.risk_score
    
    # Convert to list format
    trends = []
    for date_str in sorted(daily_data.keys()):
        data = daily_data[date_str]
        trends.append({
            "date": date_str,
            "total": data['total'],
            "fraud": data['fraud'],
            "average_risk": data['risk_sum'] / data['total'] if data['total'] > 0 else 0
        })
    
    # Return last 'days' worth of data
    return trends[-days:] if len(trends) > days else trends

@router.get("/alerts")
async def get_alerts(
    resolved: bool = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    query = select(Alert).order_by(Alert.created_at.desc()).limit(limit)
    
    if resolved is not None:
        query = query.where(Alert.resolved == resolved)
    
    result = await db.execute(query)
    alerts = result.scalars().all()
    
    return [{
        "id": a.id,
        "transaction_id": a.transaction_id,
        "alert_type": a.alert_type,
        "severity": a.severity,
        "message": a.message,
        "resolved": a.resolved,
        "created_at": a.created_at.isoformat()
    } for a in alerts]