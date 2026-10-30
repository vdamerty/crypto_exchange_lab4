
import random
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker("uk_UA")
Faker.seed(42)
random.seed(42)

Path("data_lake").mkdir(exist_ok=True)

# 1. Трейдери
traders = pd.DataFrame([
    {
        "trader_id": i,
        "full_name": fake.name(),
        "email": fake.email() if random.random() > 0.1 else None,
        "registered_at": fake.date_between(
            start_date="-2y", end_date="today"
        )
    }
    for i in range(1, 101)
])

# Додаємо дублікати для подальшого очищення в dbt
traders = pd.concat([
    traders,
    traders.sample(frac=0.05, random_state=42)
], ignore_index=True)

# 2. Криптовалюти
currencies = pd.DataFrame([
    {"currency_id": 1, "symbol": "BTC", "price_usd": 65000},
    {"currency_id": 2, "symbol": "ETH", "price_usd": 3200},
    {"currency_id": 3, "symbol": "SOL", "price_usd": 150},
    {"currency_id": 4, "symbol": "ADA", "price_usd": 0.5},
    {"currency_id": 5, "symbol": "USDT", "price_usd": 1}
])

# 3. Гаманці
wallet_list = []
wallet_id = 1

for trader_id in range(1, 101):
    for currency_id in range(1, 6):
        wallet_list.append({
            "wallet_id": wallet_id,
            "trader_id": trader_id,
            "currency_id": currency_id,
            "balance": round(random.uniform(0, 10), 4)
        })
        wallet_id += 1

wallets = pd.DataFrame(wallet_list)

# Функція випадкової дати
def random_date():
    start = datetime(2025, 11, 1)
    return start + timedelta(
        days=random.randint(0, 360),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

# 4. Торгові угоди
trades_list = []

for i in range(1, 2001):
    wallet = random.choice(wallet_list)
    currency = currencies.iloc[wallet["currency_id"] - 1]

    quantity = round(random.uniform(0.001, 2), 4)
    price = round(
        float(currency["price_usd"]) * random.uniform(0.9, 1.1), 4
    )

    trades_list.append({
        "trade_id": i,
        "trader_id": wallet["trader_id"],
        "wallet_id": wallet["wallet_id"],
        "currency_id": wallet["currency_id"],
        "trade_type": random.choice(["buy", "sell"]),
        "quantity": quantity,
        "price_usd": price,
        "total_usd": round(quantity * price, 2),
        "trade_date": random_date()
    })

trades = pd.DataFrame(trades_list)

# 5. Поповнення та виведення коштів
operations = []

for i in range(1, 801):
    wallet = random.choice(wallet_list)

    operations.append({
        "transaction_id": i,
        "wallet_id": wallet["wallet_id"],
        "trader_id": wallet["trader_id"],
        "currency_id": wallet["currency_id"],
        "operation_type": random.choice([
            "deposit", "withdrawal"
        ]),
        "amount": round(random.uniform(0.01, 5), 4),
        "created_at": random_date()
    })

deposits_withdrawals = pd.DataFrame(operations)

# Збереження у Parquet
tables = {
    "traders": traders,
    "currencies": currencies,
    "wallets": wallets,
    "trades": trades,
    "deposits_withdrawals": deposits_withdrawals
}

for name, df in tables.items():
    df.to_parquet(f"data_lake/{name}.parquet", index=False)
    print(f"{name}: {len(df)} записів")

print("Генерацію даних завершено успішно")
