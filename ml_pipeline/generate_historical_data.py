import requests
import random
import time
from datetime import datetime, timedelta
import sys

API_URL = "http://localhost:8000/api/v1/transactions/score"

class HistoricalDataGenerator:
    def __init__(self):
        self.user_pools = {
            'normal': [f"USER_{i}" for i in range(1000, 1200)],
            'suspicious': [f"USER_{i}" for i in range(5000, 5020)]
        }
    
    def generate_transaction(self, fraud_likelihood=0.1):
        """Generate a transaction with specified fraud likelihood"""
        is_fraud_pattern = random.random() < fraud_likelihood
        
        if is_fraud_pattern:
            # High-risk transaction
            return {
                "user_id": random.choice(self.user_pools['suspicious']),
                "merchant_id": f"MERCHANT_{random.randint(800, 999)}",
                "amount": round(random.uniform(3000, 15000), 2),
                "currency": "USD",
                "country": random.choice(['US', 'NG', 'RU', 'PK']),
                "device_id": f"DEVICE_{random.randint(5000, 5100)}",
                "ip_address": f"45.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "transaction_type": random.choice(['transfer', 'withdrawal']),
                "channel": "web"
            }
        else:
            # Normal transaction
            return {
                "user_id": random.choice(self.user_pools['normal']),
                "merchant_id": f"MERCHANT_{random.randint(100, 500)}",
                "amount": round(random.uniform(10, 1000), 2),
                "currency": "USD",
                "country": random.choice(['US', 'UK', 'CA', 'DE', 'FR']),
                "device_id": f"DEVICE_{random.randint(1000, 2000)}",
                "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "transaction_type": random.choice(['purchase', 'transfer']),
                "channel": random.choice(['web', 'mobile', 'pos'])
            }

def send_transaction(txn):
    """Send transaction to API"""
    try:
        response = requests.post(API_URL, json=txn, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_day_data(day_offset, num_transactions, fraud_rate):
    """Generate transactions for a specific day"""
    date = datetime.now() - timedelta(days=day_offset)
    date_str = date.strftime('%Y-%m-%d')
    
    print(f"\n📅 Generating {num_transactions} transactions for {date_str} (fraud rate: {fraud_rate*100:.0f}%)")
    
    generator = HistoricalDataGenerator()
    successful = 0
    fraud_detected = 0
    
    for i in range(num_transactions):
        txn = generator.generate_transaction(fraud_likelihood=fraud_rate)
        result = send_transaction(txn)
        
        if result:
            successful += 1
            if result['is_fraud']:
                fraud_detected += 1
            
            # Show progress
            if (i + 1) % 10 == 0:
                print(f"  ✓ {i + 1}/{num_transactions} transactions processed...")
        
        time.sleep(0.1)  # Don't overwhelm the API
    
    print(f"  ✅ {date_str}: {successful} transactions, {fraud_detected} fraud detected")
    return successful, fraud_detected

def main():
    print("\n" + "="*80)
    print("📊 HISTORICAL FRAUD DETECTION DATA GENERATOR")
    print("="*80)
    print("\nGenerating 7 days of historical transaction data...\n")
    
    # Define daily patterns (transactions per day, fraud rate)
    daily_patterns = [
        # (days_ago, num_transactions, fraud_rate)
        (6, 45, 0.04),   # 6 days ago - low activity, low fraud
        (5, 62, 0.08),   # 5 days ago - medium activity, rising fraud
        (4, 58, 0.05),   # 4 days ago - normal day
        (3, 71, 0.11),   # 3 days ago - high activity, high fraud spike
        (2, 55, 0.07),   # 2 days ago - cooling down
        (1, 68, 0.09),   # yesterday - building up
        (0, 73, 0.12),   # today - highest fraud rate
    ]
    
    total_transactions = 0
    total_fraud = 0
    
    for days_ago, num_txns, fraud_rate in daily_patterns:
        success, fraud = generate_day_data(days_ago, num_txns, fraud_rate)
        total_transactions += success
        total_fraud += fraud
    
    print("\n" + "="*80)
    print(f"✅ Historical data generation complete!")
    print(f"📊 Total: {total_transactions} transactions, {total_fraud} fraud detected")
    print(f"🔴 Overall fraud rate: {(total_fraud/total_transactions)*100:.1f}%")
    print("="*80)
    print("\n🎯 Now refresh your dashboard at http://localhost:3000 to see the trend!\n")

if __name__ == "__main__":
    print("\n⚠️  Note: This will create ~430 transactions across 7 days.")
    print("    It will take about 5-7 minutes to complete.\n")
    
    response = input("Continue? (y/n): ")
    if response.lower() == 'y':
        main()
    else:
        print("Cancelled.")