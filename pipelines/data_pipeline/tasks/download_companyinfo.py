import requests
import pandas as pd
import numpy as np
import os
from pathlib import Path
from data_fetching.edgar_helpers import parse_companyfact_dict, extract_data
from utils.logging_utils import setup_logging

def fetch_companyfacts(user_agent, logger):
    SEC_URL = 'https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip'
    LOCAL_PATH = Path('data/companyfacts.zip')
    
    def check_local_file():
        if LOCAL_PATH.exists():
            logger.debug(f"Found local file at {LOCAL_PATH}")
            return str(LOCAL_PATH)
        logger.warning("Local file not found")
        return None

    while True:
        fetch_online = input("Fetch online (y/n): ").lower()
        if fetch_online in ('y', 'n'):
            break
        print("Please enter 'y' or 'n'")

    if fetch_online == 'y':
        headers = {
            'User-Agent': user_agent,
            'Accept-Encoding': 'gzip, deflate'
        }
        
        try:
            logger.debug(f"Fetching from {SEC_URL}...")
            resp = requests.get(SEC_URL, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                logger.debug("Request successful (status code 200)")
                return resp
            
            logger.error(f"Request failed (status code {resp.status_code})")
            return check_local_file()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return check_local_file()
    
    return check_local_file()

def main():
    logger = setup_logging()
    user_agent = 'MyCompanyName (myemail@example.com)'
    
    os.makedirs('data', exist_ok=True)
    source = fetch_companyfacts(user_agent, logger)
    
    if source is not None:
        try:
            data_list = extract_data(source, logger, extraction_dir='data/')
            if data_list:
                df = pd.DataFrame(data_list)
                
                # output_path = Path('data/companyfacts.csv')
                # df.to_csv(output_path, index=False)
                # logger.info(f"Data saved to {output_path}")
                parquet_path = Path('data/companyfacts.parquet')
                df.to_parquet(parquet_path, index=False)
                logger.info(f"Data saved to {parquet_path}")
                
                # return df
            else:
                logger.warning("No data extracted")
                return None
                
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            return None
    else:
        logger.error("No data source available")
        return None

if __name__ == "__main__":
    main()
    # if df is not None:
    #     print(f"DataFrame shape: {df.shape}")
    #     print("\nFirst few rows:")
    #     print(df.head())
    #     print("\nColumns:")
    #     print(df.columns.tolist())