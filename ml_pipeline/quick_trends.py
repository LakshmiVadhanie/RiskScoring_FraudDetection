import requests
import random
from datetime import datetime, timedelta

API_URL = "http://localhost:8000/api/v1/transactions/score"

def quick_transaction():
    return {
        "user_id": f"USER_{random.randint(1000, 9999)}",
        "merchant_id": f"MERCHANT_{random.randint(100, 999)}",
        "amount": round(random.uniform(50, 3000), 2),
        "currency": "USD",
        "country": random.choice(['US', 'UK', 'CA', 'NG']),
        "device_id": f"DEVICE_{random.randint(1000, 5000)}",
        "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
        "transaction_type": random.choice(['purchase', 'transfer']),
        "channel": random.choice(['web', 'mobile'])
    }

print("⚡ Quick trend data generator (20 transactions per day for 7 days)")

for day in range(6, -1, -1):
    date = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d')
    print(f"Generating {date}...", end=" ")
    
    for _ in range(20):
        try:
            requests.post(API_URL, json=quick_transaction(), timeout=2)
        except:
            pass
    
    print("✓")
