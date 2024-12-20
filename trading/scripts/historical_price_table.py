import yaml
import os
import psycopg2
from trading.utils.logging_config import setup_logging
import logging

setup_logging()

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
print(root_dir)
db_yaml = os.path.join(root_dir, 'config', 'db_settings.yaml')
print(db_yaml)
with open(db_yaml, 'r') as file:
    DB_CONFIG = yaml.safe_load(file)['postgres']
    
    
def create_table():
    scheme = '''
    CREATE TABLE IF NOT EXISTS historical_daily_prices (
        id SERIAL PRIMARY KEY,
        ticker VARCHAR(10) NOT NULL,
        date DATE NOT NULL,
        open_price FLOAT,
        high_price FLOAT,
        low_price FLOAT,
        close_price FLOAT,
        adjusted_close FLOAT,
        volume BIGINT,
        source VARCHAR(50),
        created_at TIMESTAMP DEFAULT NOW(),
        UNIQUE (ticker, date)
        );
        '''
    try:
        logging.info("Connecting to DB")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(scheme)
        conn.commit()
        logging.info("Table 'historical_prices' created successfully")
        cursor.close()
        conn.close()
        logging.info("Database connection closed.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    create_table()

