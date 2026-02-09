import requests
import random
import time

API_URL = "http://localhost:8000/api/v1/transactions/score"

def generate_transaction():
    return {
        "user_id": f"USER_{random.randint(1000, 9999)}",
        "merchant_id": f"MERCHANT_{random.randint(100, 999)}",
        "amount": round(random.uniform(10, 5000), 2),
        "currency": "USD",
        "country": random.choice(['US', 'UK', 'CA', 'DE', 'FR', 'NG', 'RU']),
        "device_id": f"DEVICE_{random.randint(1000, 9999)}",
        "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
        "transaction_type": random.choice(['purchase', 'transfer', 'withdrawal']),
        "channel": random.choice(['web', 'mobile', 'pos'])
    }

def main():
    print("Generating sample transactions...")
    for i in range(50):
        txn = generate_transaction()
        try:
            response = requests.post(API_URL, json=txn)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Transaction {i+1}: Risk={result['risk_score']:.2f}, Decision={result['decision']}")
            else:
                print(f"✗ Failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Error: {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()