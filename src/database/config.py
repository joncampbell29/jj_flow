from utils.env_utils import _load_root_env, _get_proj_root
import os
import yaml
# import typing

def get_db_config(db_config_yaml_path:str=None)->dict[str, str]:
    """
    Get the database configuration from the environment variables or a YAML file.
    
    Parameters
    ----------
    db_config_yaml_path : str, optional
        The path to the YAML file containing the database configuration. If not provided, the default path  from database.config._get_proj_root is used.

    Returns
    -------
    Dict
        A dictionary containing the database configuration.
    """
    root_dir = _get_proj_root()
    _load_root_env()
    try:
        yaml_path = db_config_yaml_path if db_config_yaml_path else os.path.join(root_dir, "config/db_default_config.yaml")
        with open(yaml_path, "r") as f:
            default_config = yaml.safe_load(f)
    except FileNotFoundError:
        raise RuntimeError(f".yaml file could not be found: {yaml_path}")
    except yaml.YAMLError as e:
        raise RuntimeError(f"Error reading YAML config file: {e}")
        
    db_config = {
        "host": os.getenv("DB_HOST", default_config["default"]["host"]),
        "port": os.getenv("DB_PORT", default_config["default"]["port"]),
        "dbname": os.getenv("DB_NAME", default_config["default"]["dbname"]),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD")
        }
    required_vals = ['host', 'port', 'dbname', 'user', 'password']
    for key in required_vals:
        if not db_config.get(key):
            raise ValueError(f"Missing required DB config key: {key}")
        
    return db_config
