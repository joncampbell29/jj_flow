import json
import zipfile
import requests
from io import BytesIO
import re
import os
import pandas as pd


def parse_addresses(address_val):
    return_dict = {
        'stateorcountry_mailing': None,
        'stateorcountry_business': None
    }
    def parse_type(addy_dict):
        parts = [
            addy_dict.get('street1'),
            addy_dict.get('street2'),
            addy_dict.get('city'),
            addy_dict.get('stateOrCountry'),
            addy_dict.get('zipCode'),
            # address_val['mailing'].get('stateOrCountryDescription')
            ]
        parts = [part for part in parts if part]
        return ', '.join(parts) if len(parts) != 0 else None
        
    if 'mailing' in address_val:
        return_dict['stateorcountry_mailing'] = parse_type(address_val['mailing'])
            
    if 'business' in address_val:
        return_dict['stateorcountry_business'] = parse_type(address_val['business'])
    return return_dict

def parse_companyfact_dict(companyfact_dict):
    wanted_info = {
        'filepath', 'cik', 'name', 'tickers', 'exchanges',
        'ein', 'description', 'website', 'investorWebsite', 
        'category', 'fiscalYearEnd', 'stateOfIncorporation', 'entityType',
        'sic', 'sicDescription', 'ownerOrg', 
        'addresses',  'phone', 'formerNames'
    }
    return_dict = {info: None for info in wanted_info}
    for key in list(return_dict.keys()):
        if key == 'exchanges':
            if len(companyfact_dict['exchanges']) != 0: 
                return_dict['exchanges'] = ",".join(companyfact_dict['exchanges'])
        elif key == 'tickers':
            if len(companyfact_dict['tickers']) != 0: 
                return_dict['tickers'] = ",".join(companyfact_dict['tickers'])
        elif key == 'formerNames':
            if len(companyfact_dict['formerNames']) != 0:  
                return_dict['formerNames'] = ",".join([i['name'] for i in companyfact_dict['formerNames']])
        elif key == 'addresses':
            res = parse_addresses(companyfact_dict['addresses'])
            return_dict['stateorcountry_mailing'] = res['stateorcountry_mailing']
            return_dict['stateorcountry_business'] = res['stateorcountry_business']
        else:
            return_dict[key] = companyfact_dict[key] if companyfact_dict[key] != '' else None
    return_dict.pop("addresses")
    return return_dict

def extract_data(source):
    
    return_dat = []
    extract_folder = 'data/'
    if isinstance(source, requests.models.Response):
        zip_path = BytesIO(source.content)
    elif isinstance(source, str):
        zip_path = source
    with zipfile.ZipFile(zip_path) as z:
        file_list = z.namelist()
        pattern = re.compile(r'^CIK\d+\.json$')
        file_list = [f for f in file_list if pattern.match(f)]
        
        for file in file_list:
            z.extract(file, extract_folder)
            json_path = os.path.join(extract_folder, file)
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                data['filepath'] = file
                return_dat.append(parse_companyfact_dict(data))
            
            # add deletion of file
    return pd.Dataframe(return_dat)
