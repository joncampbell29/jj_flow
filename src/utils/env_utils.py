import os
from dotenv import load_dotenv

def _get_proj_root():
    cur_path = os.path.dirname(__file__)
    while True:
        if ".env" in os.listdir(cur_path):
            return cur_path
        parent = os.path.dirname(cur_path)
        if parent == cur_path:
            raise FileNotFoundError(".env file not found in any parent directory")
        cur_path = parent

def _load_root_env():
    proj_root = _get_proj_root()
    env_path = os.path.join(proj_root,".env")
    load_dotenv(dotenv_path=env_path)
