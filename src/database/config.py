import os

def get_db_config()->dict[str, str]:
    """
    Get the database configuration from .env
    
    Parameters
    ----------
        None
    Returns
    -------
    Dict
        A dictionary containing the database configuration.
    """
    db_config = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
        }
    required_vals = ['host', 'port', 'dbname', 'user', 'password']
    for key in required_vals:
        if not db_config.get(key):
            raise ValueError(f"Missing required DB config key: {key}")
        
    return db_config
