from utils.env_utils import _load_root_env
import os

def get_alpaca_keys(api_key_name="ALPACA_PAPER_API_KEY", secret_key_name="ALPACA_PAPER_SECRET"):
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
