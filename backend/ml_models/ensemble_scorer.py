import numpy as np
from typing import Dict

class EnsembleScorer:
    def __init__(self):
        self.models = {
            'xgboost': self._xgboost_score,
            'isolation_forest': self._anomaly_score,
            'rule_based': self._rule_based_score,
            'graph_network': self._graph_score
        }
    
    def predict(self, features: np.ndarray) -> Dict:
        """Ensemble prediction from multiple models"""
        scores = {}
        
        for model_name, model_func in self.models.items():
            scores[model_name] = model_func(features)
        
        # Weighted ensemble
        weights = {'xgboost': 0.4, 'isolation_forest': 0.25, 'rule_based': 0.20, 'graph_network': 0.15}
        ensemble_score = sum(scores[k] * weights[k] for k in scores)
        
        # Generate reasons
        reasons = self._generate_reasons(features, scores)
        
        return {
            'ensemble_score': float(ensemble_score),
            'model_scores': {k: float(v) for k, v in scores.items()},
            'reasons': reasons,
            'fraud_probability': float(ensemble_score)
        }
    
    def _xgboost_score(self, features: np.ndarray) -> float:
        """Simulated XGBoost prediction"""
        amount_risk = min(features[0] / 5000, 1.0)
        velocity_risk = min(features[2] / 5, 1.0)
        return amount_risk * 0.6 + velocity_risk * 0.4
    
    def _anomaly_score(self, features: np.ndarray) -> float:
        """Simulated anomaly detection"""
        mean_features = np.array([150, 3, 2, 1, 12, 0, 0, 0, 0])
        std_features = np.array([300, 2, 3, 2, 6, 1, 1, 1, 1])
        
        z_scores = np.abs((features - mean_features) / (std_features + 1e-6))
        return min(np.mean(z_scores) / 4, 1.0)
    
    def _rule_based_score(self, features: np.ndarray) -> float:
        """Rule-based risk scoring"""
        risk = 0.0
        
        # High amount
        if features[0] > 5000:
            risk += 0.3
        
        # High velocity
        if features[2] > 5:
            risk += 0.4
        
        # Night transaction
        if features[5] == 1:
            risk += 0.2
        
        # High risk country
        if features[8] == 1:
            risk += 0.3
        
        return min(risk, 1.0)
    
    def _graph_score(self, features: np.ndarray) -> float:
        """Network-based risk"""
        device_count = features[3]
        if device_count > 5:
            return 0.8
        elif device_count > 3:
            return 0.5
        return 0.2
    
    def _generate_reasons(self, features: np.ndarray, scores: Dict) -> list:
        """Generate explainable reasons"""
        reasons = []
        
        if features[0] > 2000:
            reasons.append(f"High transaction amount: ${features[0]:.2f}")
        
        if features[2] > 3:
            reasons.append(f"High velocity: {int(features[2])} recent transactions")
        
        if features[5] == 1:
            reasons.append("Unusual time: Transaction during night hours")
        
        if features[8] == 1:
            reasons.append("High-risk country detected")
        
        if features[3] > 3:
            reasons.append(f"Multiple devices: {int(features[3])} devices used")
        
        if scores['isolation_forest'] > 0.7:
            reasons.append("Anomalous transaction pattern detected")
        
        return reasons if reasons else ["Normal transaction pattern"]