import psycopg2
from datetime import datetime, timedelta
import random

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="fraud_detection",
    user="frauduser",
    password="fraudpass123"
)

cursor = conn.cursor()

# Get all transactions
cursor.execute("SELECT id FROM transactions ORDER BY created_at")
transaction_ids = [row[0] for row in cursor.fetchall()]

total_txns = len(transaction_ids)
print(f"Found {total_txns} transactions to backdate")

# Distribute across 7 days
days = 7
txns_per_day = total_txns // days

for day in range(days):
    start_idx = day * txns_per_day
    end_idx = start_idx + txns_per_day if day < days - 1 else total_txns
    
    # Random time within that day
    base_date = datetime.now() - timedelta(days=(days - 1 - day))
    
    for i in range(start_idx, end_idx):
        txn_id = transaction_ids[i]
        
        # Random time within the day
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)
        
        new_timestamp = base_date.replace(
            hour=random_hour,
            minute=random_minute,
            second=random_second,
            microsecond=0
        )
        
        cursor.execute(
            "UPDATE transactions SET created_at = %s WHERE id = %s",
            (new_timestamp, txn_id)
        )
    
    print(f"✓ Day {day + 1}: {end_idx - start_idx} transactions backdated")

conn.commit()
print("\n✅ All transactions backdated successfully!")

# Show distribution
cursor.execute("""
    SELECT 
        DATE(created_at) as date,
        COUNT(*) as total,
        SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) as fraud
    FROM transactions
    GROUP BY DATE(created_at)
    ORDER BY date
""")

print("\n📊 Transaction Distribution:")
print("-" * 60)
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} transactions ({row[2]} fraud)")

cursor.close()
conn.close()