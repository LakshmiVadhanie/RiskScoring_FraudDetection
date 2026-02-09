from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    merchant_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    country = Column(String, nullable=False)
    device_id = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    is_fraud = Column(Boolean, nullable=False)
    fraud_probability = Column(Float, nullable=False)
    decision = Column(String, nullable=False)
    
    model_scores = Column(JSON)
    reasons = Column(JSON)
    
    created_at = Column(DateTime, default=func.now(), index=True)
    
    reviewed = Column(Boolean, default=False)
    actual_fraud = Column(Boolean, nullable=True)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String, nullable=False)
    alert_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)
    details = Column(JSON)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())