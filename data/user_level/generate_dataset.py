"""
Generates a synthetic transaction dataset for ML practice.

Simulates per-household spending behavior with:
- Recurring payments (rent, utilities)
- Category-level spending patterns
- ~2% injected anomalies
- Time-based train/test split
"""

import pandas as pd
import numpy as np

np.random.seed(42)

N_HOUSEHOLDS = 120
N_DAYS = 180
TRANSACTIONS_PER_DAY = 3
ANOMALY_RATE = 0.02

rows = []

for household_id in range(N_HOUSEHOLDS):
    base_spending = np.random.uniform(50, 300)

    for day in range(N_DAYS):
        date = pd.Timestamp("2024-01-01") + pd.Timedelta(days=day)

        for _ in range(TRANSACTIONS_PER_DAY):
            amount = np.random.normal(base_spending, 50)
            category = np.random.choice(
                ["groceries", "rent", "utilities", "health", "entertainment"]
            )

            is_recurring = int(category in ["rent", "utilities"] and day % 30 == 0)

            is_anomalous = int(np.random.rand() < ANOMALY_RATE)
            if is_anomalous:
                amount *= np.random.uniform(3, 8)

            rows.append({
                "household_id": household_id,
                "date": date,
                "amount": round(max(5.0, amount), 2),
                "category": category,
                "is_recurring": is_recurring,
                "is_anomalous": is_anomalous,
            })

df = pd.DataFrame(rows)
df = df.sort_values(["household_id", "date"]).reset_index(drop=True)

# Time-based split (80/20)
split_date = df["date"].quantile(0.8)
train = df[df["date"] <= split_date]
test = df[df["date"] > split_date]

import os
os.makedirs("data/user_level", exist_ok=True)

train.to_csv("data/user_level/transactions_train.csv", index=False)
test.drop(columns=["is_anomalous"]).to_csv("data/user_level/transactions_test.csv", index=False)
test[["household_id", "date", "is_anomalous"]].to_csv("data/user_level/transactions_test_labels.csv", index=False)
df.to_csv("data/user_level/transactions_full.csv", index=False)

print(f"Dataset generated: {len(df):,} rows across {N_HOUSEHOLDS} households")
print(f"Train: {len(train):,} rows | Test: {len(test):,} rows")
print(f"Anomaly rate: {df['is_anomalous'].mean():.2%}")
print()
print("Files saved to data/user_level/")
