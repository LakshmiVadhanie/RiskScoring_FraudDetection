export interface Transaction {
  id: string;
  user_id: string;
  merchant_id: string;
  amount: number;
  currency: string;
  country: string;
  device_id: string;
  risk_score: number;
  risk_level: 'MINIMAL' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  is_fraud: boolean;
  fraud_probability: number;
  decision: 'APPROVE' | 'REVIEW' | 'BLOCK';
  reasons: string[];
  model_scores: Record<string, number>;
  created_at: string;
}

export interface DashboardStats {
  total_transactions: number;
  fraud_detected: number;
  fraud_rate: number;
  average_risk_score: number;
  total_amount_processed: number;
  risk_distribution: Record<string, number>;
  decision_distribution: Record<string, number>;
  unresolved_alerts: number;
}

export interface Alert {
  id: number;
  transaction_id: string;
  alert_type: string;
  severity: string;
  message: string;
  resolved: boolean;
  created_at: string;
}

export interface TrendData {
  date: string;
  total: number;
  fraud: number;
  average_risk: number;
}