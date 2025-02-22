import requests
import pandas as pd
import numpy as np
import zipfile
import os
import json
import re
from io import BytesIO
import logging
import logging.config
import yaml
from data_fetching.edgar_helpers import parse_companyfact_dict, extract_data

with open('config/logging_config.yaml', 'r') as fil:
    config = yaml.safe_load(fil.read())
logging.config.dictConfig(config)
logger = logging.getLogger('data_pipeline')


user_agent = 'MyCompanyName (myemail@example.com)'
fetch_online = input(f"Fetch online (y/n): ")
if fetch_online.lower() == 'y':
    headers = {
        'User-Agent': user_agent,
        'Accept-Encoding': 'gzip, deflate'
        }
    url = 'https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip'
    
    logger.debug(f"fetching from {url}")
    resp = requests.get(url, headers=headers)
        
    if resp.status_code == 200:
        logger.debug("Request Success, status code 200!!")
    else:
        logger.error(f"Request Fail, status code {resp.status_code}")
        logger.debug("Checking data/ for companyfacts.zip...")
        if 'companyfacts.zip' in os.listdir('data/'):
            url = "data/companyfacts.zip"
            logger.debug("Extracting from data/companyfacts.zip")
        else:
            logger.warning("Could not get data")
else:
    if 'companyfacts.zip' in os.listdir('data/'):
        url = "data/companyfacts.zip"
        # logger.debug("Extracting from data/companyfacts.zip")
    else:
        logger.warning("Could not get data")
    

