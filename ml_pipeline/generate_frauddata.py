import requests
import random
import time
from datetime import datetime

API_URL = "http://localhost:8000/api/v1/transactions/score"

# Fraud patterns based on your ML model
class FraudGenerator:
    def __init__(self):
        self.user_pools = {
            'normal': [f"USER_{i}" for i in range(1000, 1100)],
            'suspicious': [f"USER_{i}" for i in range(5000, 5010)]
        }
        self.device_pools = {
            'normal': [f"DEVICE_{i}" for i in range(1000, 1200)],
            'shared': [f"DEVICE_SHARED_{i}" for i in range(1, 5)]
        }
    
    def normal_transaction(self):
        """Low-risk normal transaction"""
        return {
            "user_id": random.choice(self.user_pools['normal']),
            "merchant_id": f"MERCHANT_{random.randint(100, 500)}",
            "amount": round(random.uniform(10, 500), 2),
            "currency": "USD",
            "country": random.choice(['US', 'UK', 'CA', 'DE', 'FR']),
            "device_id": random.choice(self.device_pools['normal']),
            "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "transaction_type": random.choice(['purchase', 'transfer']),
            "channel": random.choice(['web', 'mobile', 'pos'])
        }
    
    def high_amount_fraud(self):
        """High amount transaction (triggers amount-based detection)"""
        return {
            "user_id": random.choice(self.user_pools['suspicious']),
            "merchant_id": f"MERCHANT_{random.randint(800, 999)}",
            "amount": round(random.uniform(8000, 25000), 2),  # Very high!
            "currency": "USD",
            "country": random.choice(['US', 'UK']),
            "device_id": f"DEVICE_{random.randint(3000, 3100)}",
            "ip_address": f"10.0.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "transaction_type": "transfer",
            "channel": "web"
        }
    
    def velocity_fraud(self):
        """Multiple transactions from same user (triggers velocity detection)"""
        user_id = random.choice(self.user_pools['suspicious'])
        return {
            "user_id": user_id,  # Same user, multiple times
            "merchant_id": f"MERCHANT_{random.randint(100, 999)}",
            "amount": round(random.uniform(200, 1000), 2),
            "currency": "USD",
            "country": "US",
            "device_id": f"DEVICE_{random.randint(1000, 2000)}",
            "ip_address": f"172.16.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "transaction_type": "purchase",
            "channel": "mobile"
        }
    
    def high_risk_country(self):
        """Transaction from high-risk country"""
        return {
            "user_id": random.choice(self.user_pools['normal']),
            "merchant_id": f"MERCHANT_{random.randint(100, 999)}",
            "amount": round(random.uniform(500, 3000), 2),
            "currency": "USD",
            "country": random.choice(['NG', 'RU', 'CN', 'PK']),  # High-risk countries
            "device_id": f"DEVICE_{random.randint(1000, 2000)}",
            "ip_address": f"45.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "transaction_type": "transfer",
            "channel": "web"
        }
    
    def night_transaction(self):
        """Transaction during unusual hours"""
        return {
            "user_id": random.choice(self.user_pools['normal']),
            "merchant_id": f"MERCHANT_{random.randint(100, 999)}",
            "amount": round(random.uniform(1000, 5000), 2),
            "currency": "USD",
            "country": "US",
            "device_id": f"DEVICE_{random.randint(1000, 2000)}",
            "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "transaction_type": "withdrawal",
            "channel": "web"
        }
    
    def device_sharing(self):
        """Multiple users on same device (account takeover pattern)"""
        shared_device = random.choice(self.device_pools['shared'])
        return {
            "user_id": f"USER_{random.randint(1000, 9999)}",  # Different users
            "merchant_id": f"MERCHANT_{random.randint(100, 999)}",
            "amount": round(random.uniform(500, 2000), 2),
            "currency": "USD",
            "country": "US",
            "device_id": shared_device,  # Same device!
            "ip_address": f"192.168.1.{random.randint(1, 50)}",
            "transaction_type": "purchase",
            "channel": "mobile"
        }

def send_transaction(txn, category):
    try:
        response = requests.post(API_URL, json=txn)
        if response.status_code == 200:
            result = response.json()
            risk = result['risk_score'] * 100
            color = "🟢" if risk < 40 else "🟡" if risk < 60 else "🔴"
            print(f"{color} {category:20} | Risk: {risk:5.1f}% | Decision: {result['decision']:7} | Amount: ${txn['amount']:>10,.2f}")
            return result
        else:
            print(f"❌ Failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("\n" + "="*100)
    print("🚨 FRAUD DETECTION TESTING - Generating Diverse Transactions")
    print("="*100 + "\n")
    
    generator = FraudGenerator()
    
    # Mix of transaction types
    scenarios = [
        ("Normal Transaction", generator.normal_transaction, 20),
        ("High Amount Fraud", generator.high_amount_fraud, 8),
        ("Velocity Attack", generator.velocity_fraud, 10),
        ("High-Risk Country", generator.high_risk_country, 6),
        ("Night Transaction", generator.night_transaction, 4),
        ("Device Sharing", generator.device_sharing, 12),
    ]
    
    total = 0
    high_risk = 0
    
    for category, func, count in scenarios:
        print(f"\n📊 Generating {count} {category}s...")
        print("-" * 100)
        for i in range(count):
            txn = func()
            result = send_transaction(txn, category)
            if result and result['risk_score'] >= 0.6:
                high_risk += 1
            total += 1
            time.sleep(0.3)  # Don't overwhelm the API
    
    print("\n" + "="*100)
    print(f"✅ Generated {total} transactions")
    print(f"🔴 High-risk detected: {high_risk} ({(high_risk/total)*100:.1f}%)")
    print("="*100 + "\n")
    
    print("🎯 Now refresh your dashboard at http://localhost:3000 to see the results!\n")

if __name__ == "__main__":
    main()