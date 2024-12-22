from utils.env_utils import _load_root_env
import os
# import typing

def get_alpaca_keys(api_key_name:str="ALPACA_PAPER_API_KEY", secret_key_name:str="ALPACA_PAPER_SECRET")-> dict[str, str]:
    """
    Get Alpaca API keys from .env file.
    
    Parameters
    ----------
    api_key_name: str
        api key name for the api key in the .env file
    secret_key_name: str
        api secret key name for the secret key in the .env file

    Returns
    -------
    Dict
        A dictionary containing the api and secrete key
    """
    _load_root_env()
    
    credentials_dict = {
        'api_key': os.getenv(api_key_name),
        'secret_key': os.getenv(secret_key_name)
    }
    for name, val in credentials_dict.items():
        if not credentials_dict[name]:
            if name == 'api_key':
                raise ValueError(f"{name+'_name'} {api_key_name} not found in .env")
            else:
                raise ValueError(f"{name+'_name'} {secret_key_name} not found in .env")
    return credentials_dict
