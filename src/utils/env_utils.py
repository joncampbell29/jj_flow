import os
from dotenv import load_dotenv

def get_proj_root()->str:
    """
    Traverses files and returns the directory where a .env file is found.
    
    Parameters
    ----------
    None

    Returns
    -------
    str
        The path to the directory containing the .env file
    """
    cur_path = os.path.dirname(__file__)
    while True:
        if ".env" in os.listdir(cur_path):
            return cur_path
        parent = os.path.dirname(cur_path)
        if parent == cur_path:
            raise FileNotFoundError(".env file not found in any parent directory")
        cur_path = parent

def load_root_env()->None:
    """
    Loads the .env file in the directory found by get_proj_root()
    
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    proj_root = get_proj_root()
    env_path = os.path.join(proj_root,".env")
    load_dotenv(dotenv_path=env_path)
