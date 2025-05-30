import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def generate_sample_data(n=10000, seed=42):
    np.random.seed(seed)
    df = pd.DataFrame({
        "transaction_id": [f"TX{i:05d}" for i in range(n)],
        "timestamp": [datetime.now() - timedelta(minutes=int(x)) for x in np.random.randint(1, 100000, n)],
        "amount": np.round(np.random.exponential(500, n), 2),
        "merchant": np.random.choice(["Amazon", "Walmart", "Starbucks", "Netflix", "Target", "Apple", "Uber", "Shell"], n),
        "location": np.random.choice(["US", "UK", "CA", "AU", "DE", "FR", "JP", "IN"], n),
        "is_fraud": np.random.binomial(1, 0.05, n)
    })
    df['risk_score'] = np.where(
        df['is_fraud'] == 1,
        np.random.randint(80, 100, n),
        np.random.randint(0, 70, n)
    )
    df['risk_category'] = pd.cut(
        df['risk_score'],
        bins=[0, 30, 70, 90, 100],
        labels=['low', 'medium', 'high', 'critical']
    )
    return df

def save_to_postgres(df, table='transactions'):
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db = os.getenv('DB_NAME')
    url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}?sslmode=require'

    try:
        engine = create_engine(url)
        df.to_sql(table, engine, if_exists='replace', index=False)
        with engine.connect() as conn:
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_risk ON transactions(risk_score)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_fraud ON transactions(is_fraud)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_amount ON transactions(amount)"))
            conn.commit()
        print("✅ Data successfully saved to PostgreSQL!")
        print(f"📊 {len(df)} rows loaded to table: {table}")
        print(f"🔍 Indexes created on risk_score, is_fraud, and amount columns")
        print(f"🌐 Database: {db} on {host}")
    except Exception as e:
        print(f"❌ Error: {e}")

def load_from_db(table='transactions'):
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    db = os.getenv('DB_NAME')
    url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}?sslmode=require'
    try:
        engine = create_engine(url)
        df = pd.read_sql_table(table, engine)
        return df
    except Exception as e:
        print(f"❌ Error loading from DB: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

if __name__ == "__main__":
    print("Generating sample data...")
    df = generate_sample_data()
    print(f"Generated {len(df)} rows of sample data")

    print("Saving to PostgreSQL...")
    save_to_postgres(df)

    print("\n✨ Next steps:")
    print("1. Go to your Neon dashboard")
    print("2. Open the SQL Editor")
    print("3. Run: SELECT * FROM transactions LIMIT 10;")