import numpy as np
from typing import Dict
from datetime import datetime

class TransactionFeatureEngine:
    def __init__(self):
        self.user_history = {}
        self.device_history = {}
    
    def extract_features(self, transaction: Dict) -> np.ndarray:
        """Extract features for ML models"""
        features = []
        
        # Amount features
        amount = transaction['amount']
        features.append(amount)
        features.append(np.log1p(amount))
        
        # Velocity features
        user_id = transaction['user_id']
        user_txn_count = self.user_history.get(user_id, 0)
        features.append(user_txn_count)
        
        # Device features
        device_id = transaction['device_id']
        device_txn_count = self.device_history.get(device_id, 0)
        features.append(device_txn_count)
        
        # Time features
        hour = datetime.now().hour
        features.append(hour)
        features.append(1 if 23 <= hour or hour <= 6 else 0)  # Night transaction
        
        # Categorical encodings
        channel_encoding = {'web': 0, 'mobile': 1, 'pos': 2}
        features.append(channel_encoding.get(transaction['channel'], 0))
        
        type_encoding = {'purchase': 0, 'transfer': 1, 'withdrawal': 2}
        features.append(type_encoding.get(transaction['transaction_type'], 0))
        
        # Country risk (simplified)
        high_risk_countries = ['NG', 'RU', 'CN', 'PK']
        features.append(1 if transaction['country'] in high_risk_countries else 0)
        
        # Update history
        self.user_history[user_id] = user_txn_count + 1
        self.device_history[device_id] = device_txn_count + 1
        
        return np.array(features, dtype=np.float32)