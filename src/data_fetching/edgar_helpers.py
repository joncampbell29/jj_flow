import json
import zipfile
import requests
from io import BytesIO
import re
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

WANTED_FIELDS = {
    'filepath', 'cik', 'name', 'tickers', 'exchanges',
    'ein', 'description', 'website', 'investorWebsite', 
    'category', 'fiscalYearEnd', 'stateOfIncorporation', 'entityType',
    'sic', 'sicDescription', 'ownerOrg', 
    'addresses', 'phone', 'formerNames'
    }

FIELD_TRANSFORMS = {
    'exchanges': lambda x: ','.join(x) if x else None,
    'tickers': lambda x: ','.join(x) if x else None,
    'formerNames': lambda x: ','.join(name['name'].strip().upper() for name in x) if x else None,
    'addresses': lambda x: parse_addresses(x),
    'name': lambda x: x.strip().upper(),
    'phone': lambda x: format_phone_number(x)
    }

def format_addy_dict(addy_dict):
        parts = [
            addy_dict.get('street1'),
            addy_dict.get('street2'),
            addy_dict.get('city'),
            addy_dict.get('stateOrCountry'),
            addy_dict.get('zipCode')
            ]
        # parts = [part for part in parts if part]
        # return ', '.join(parts) if len(parts) != 0 else None
        return ', '.join(part for part in parts if part)
    
def parse_addresses(address_val):
    return_dict = {
        'address_mailing': None,
        'address_business': None
    }
    if 'mailing' in address_val:
        return_dict['address_mailing'] = format_addy_dict(address_val['mailing'])
            
    if 'business' in address_val:
        return_dict['address_business'] = format_addy_dict(address_val['business'])
    return return_dict


def format_phone_number(phone):
    if not phone:
        return None
    # digits = ''.join(filter(str.isdigit, phone))
    digits = ''.join(c for c in phone if c.isdigit())
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone

def parse_companyfact_dict(companyfact_dict):
    
    res = {field: None for field in WANTED_FIELDS}
    for field in WANTED_FIELDS:
        val = companyfact_dict.get(field)
        if val:
            if field in FIELD_TRANSFORMS:
                transformed_val = FIELD_TRANSFORMS[field](val)
                
                if field == 'addresses':
                    res.update(transformed_val)
                else:
                    res[field] = transformed_val
            else:
                res[field] = val if val != '' else None
                
    res.pop('addresses', None)
    return dict(res)


def extract_data(source, logger, extraction_dir='data/'):
    return_dat = []
    
    os.makedirs(extraction_dir, exist_ok=True)
    
    try:
        if isinstance(source, requests.models.Response):
            zip_path = BytesIO(source.content)
        elif isinstance(source, str):
            if not os.path.exists(source):
                raise FileNotFoundError(f"ZIP file not found: {source}")
            zip_path = source
        else:
            raise ValueError("Source must be either a requests.Response or a string path")

        with zipfile.ZipFile(zip_path) as z:
            file_list = [f for f in z.namelist() if re.match(r'^CIK\d+\.json$', f)]
            logger.debug(f"{len(file_list)} files to parse")
            
            for file in file_list:
                json_path = os.path.join(extraction_dir, file)
                try:
                    z.extract(file, extraction_dir)
                    
                    with open(json_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        data['filepath'] = file
                        parsed_data = parse_companyfact_dict(data)
                        return_dat.append(parsed_data)
                        
                except zipfile.BadZipFile as e:
                    logger.error(f"Invalid ZIP file: {e}")
                    break
                except json.JSONDecodeError as e:
                    logger.warning(f"Invalid JSON in {file}: {e}")
                except Exception as e:
                    logger.warning(f"Error processing {file}: {e}")
                finally:
                    if os.path.exists(json_path):
                        os.remove(json_path)

    except Exception as e:
        logger.error(f"Failed to process ZIP file: {e}")
        raise
        
    logger.debug(f"{len(return_dat)} files successfully parsed")
    return return_dat

def process_file(file, extraction_dir, zip_path, logger):
    json_path = os.path.join(extraction_dir, file)
    
    try:
        with zipfile.ZipFile(zip_path) as z:
            z.extract(file, extraction_dir)
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data['filepath'] = file
            parsed_data = parse_companyfact_dict(data)
        
        return parsed_data
    
    except zipfile.BadZipFile as e:
        logger.error(f"Invalid ZIP file: {e}")
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON in {file}: {e}")
    except Exception as e:
        logger.warning(f"Error processing {file}: {e}")
    finally:
        if os.path.exists(json_path):
            os.remove(json_path)
    
    return None

def extract_data_parallel(source, logger, extraction_dir='data/'):
    return_dat = []
    os.makedirs(extraction_dir, exist_ok=True)
    
    try:
        if isinstance(source, requests.models.Response):
            zip_path = BytesIO(source.content)
        elif isinstance(source, str):
            if not os.path.exists(source):
                raise FileNotFoundError(f"ZIP file not found: {source}")
            zip_path = source
        else:
            raise ValueError("Source must be either a requests.Response or a string path")

        with zipfile.ZipFile(zip_path) as z:
            file_list = [f for f in z.namelist() if re.match(r'^CIK\d+\.json$', f)]
            logger.debug(f"{len(file_list)} files to parse")
            
            with ThreadPoolExecutor(max_workers=8) as executor:
                res = executor.map(lambda file: process_file(file, extraction_dir, zip_path, logger), file_list)
            
            
            return_dat = [r for r in res if r is not None]

    except Exception as e:
        logger.error(f"Failed to process ZIP file: {e}")
        raise
        
    logger.debug(f"{len(return_dat)} files successfully parsed")
    return return_dat
